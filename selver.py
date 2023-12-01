import urllib3
from bs4 import BeautifulSoup
import urllib.parse

def get_subcategories(category_box):
    subcategories = []
    subcategory_list = category_box.find('ul', class_='SidebarMenu__list')

    if subcategory_list:
        subcategory_items = subcategory_list.find_all('li', class_='SidebarMenu__item')
        for subcategory_item in subcategory_items:
            subcategory_link = subcategory_item.find('a', class_='SidebarMenu__link')
            subcategory_name = subcategory_link.find('span', class_='SidebarMenu__name').text.strip() if subcategory_link else 'Alakategooria puudub'
            subcategory_url = urllib.parse.urljoin('https://www.selver.ee', subcategory_link['href']) if subcategory_link else 'URL puudub'
            subcategories.append({'name': subcategory_name, 'url': subcategory_url})
    return subcategories

# Tee päring veebilehele
http = urllib3.PoolManager()
response = http.request('GET', 'https://www.selver.ee')
html_content = response.data.decode('utf-8')  # Vajadusel dekodeeri vastus UTF-8 vormingusse

# Kasuta BeautifulSoupi kategooriakastide leidmiseks
soup = BeautifulSoup(html_content, 'html.parser')
category_boxes = soup.find_all('li', class_='SidebarMenu__item')

# Käi läbi kõik kategooriakastid
for index, category_box in enumerate(category_boxes):
    category_button = category_box.find('button', class_='SidebarMenu__title')
    category_name = category_button.text.strip() if category_button else 'Kategooria puudub'

    # Kontrolli, kas kategooria on avatud
    is_open = 'is-open' in category_box.get('class', [])

    print(f"Kategooria #{index + 1}: {category_name}")

    # Kui kategooria on avatud, siis hangi alakategooriad
    if is_open:
        subcategories = get_subcategories(category_box)

        if subcategories:
            print("Alakategooriad:")
            for subcategory in subcategories:
                print(f"- {subcategory['name']} ({subcategory['url']})")
        else:
            print("Alakategooriad puuduvad.")
    else:
        print("Kategooria ei ole avatud.")

    print("\n")

