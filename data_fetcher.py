import requests
from bs4 import BeautifulSoup
import json
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='data_fetcher.log')
logger = logging.getLogger('DataFetcher')

class DataFetcher:
    def __init__(self, pet_manager):
        self.pet_manager = pet_manager
        
    def _extract_pet_info_from_element(self, element):
        """Trích xuất thông tin thú cưng từ một phần tử HTML với xử lý linh hoạt hơn."""
        pet_info = {'name': 'Không rõ', 'breed': 'Không rõ', 'age': 'Không rõ', 'gender': 'Không rõ'}
        
        # Tìm tên - thử nhiều selector khác nhau
        name_selectors = ['h2', '.name', '.pet-name', '[data-pet-name]']
        for selector in name_selectors:
            name_element = element.select_one(selector)
            if name_element:
                pet_info['name'] = name_element.text.strip()
                break
                
        # Tìm giống
        breed_selectors = ['.breed', '.pet-breed', '[data-breed]', 'span:contains("Breed")', 'span:contains("Giống")']
        for selector in breed_selectors:
            breed_element = element.select_one(selector)
            if breed_element:
                pet_info['breed'] = breed_element.text.strip()
                break
                
        # Tìm tuổi
        age_selectors = ['.age', '.pet-age', '[data-age]', 'span:contains("Age")', 'span:contains("Tuổi")']
        for selector in age_selectors:
            age_element = element.select_one(selector)
            if age_element:
                pet_info['age'] = age_element.text.strip()
                break
                
        # Tìm giới tính
        gender_selectors = ['.gender', '.pet-gender', '[data-gender]', 'span:contains("Gender")', 'span:contains("Giới tính")']
        for selector in gender_selectors:
            gender_element = element.select_one(selector)
            if gender_element:
                pet_info['gender'] = gender_element.text.strip()
                break
                
        return pet_info

    def fetch_pet_data_from_web(self, url):
        try:
            logger.info(f"Đang thu thập dữ liệu từ trang web: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Thử nhiều loại selector để tìm thú cưng
            pet_selectors = ['.pet-item', '.pet', '.pet-card', '.animal', '[data-pet-id]']
            pet_elements = []
            
            for selector in pet_selectors:
                elements = soup.select(selector)
                if elements:
                    pet_elements = elements
                    logger.info(f"Tìm thấy {len(elements)} thú cưng với selector {selector}")
                    break
            
            if not pet_elements:
                logger.warning(f"Không tìm thấy thú cưng trên trang {url}")
                return False
                
            for element in pet_elements:
                pet_info = self._extract_pet_info_from_element(element)
                self.pet_manager.create_pet(pet_info)

            logger.info(f"Đã thu thập thành công {len(pet_elements)} thú cưng từ: {url}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Lỗi khi truy cập {url}: {e}")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý dữ liệu từ {url}: {e}", exc_info=True)
        return False

    def fetch_pet_data_from_api(self, api_url):
        try:
            logger.info(f"Đang thu thập dữ liệu từ API: {api_url}")
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Thử nhiều cấu trúc dữ liệu API khác nhau
            pet_data_list = []
            
            if isinstance(data, list):
                pet_data_list = data
            elif isinstance(data, dict):
                for key in ['pets', 'animals', 'data', 'results', 'items']:
                    if key in data and isinstance(data[key], list):
                        pet_data_list = data[key]
                        break
                        
            if not pet_data_list:
                logger.warning(f"Không tìm thấy dữ liệu thú cưng hợp lệ trong phản hồi API từ {api_url}")
                return False
                
            # Các trường có thể chứa thông tin giống loài
            breed_fields = ['breed', 'species', 'type', 'pet_type', 'animal_type']
            
            pets_added = 0
            for item in pet_data_list:
                # Tên
                name = item.get('name', item.get('pet_name', 'Không rõ'))
                
                # Giống loài
                breed = 'Không rõ'
                for field in breed_fields:
                    if field in item and item[field]:
                        breed = item[field]
                        break
                        
                # Tuổi
                age = item.get('age', item.get('years', item.get('pet_age', 'Không rõ')))
                
                # Giới tính
                gender = item.get('gender', item.get('sex', 'Không rõ'))

                pet_info = {'name': name, 'breed': breed, 'age': age, 'gender': gender}
                self.pet_manager.create_pet(pet_info)
                pets_added += 1

            logger.info(f"Đã thu thập thành công {pets_added} thú cưng từ API: {api_url}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Lỗi khi truy cập API {api_url}: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Lỗi giải mã JSON từ API {api_url}: {e}")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý dữ liệu từ API {api_url}: {e}", exc_info=True)
        return False

