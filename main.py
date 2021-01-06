import base64
import json
import os
import jinja2
import pdfkit


base_dir = os.path.abspath(os.path.dirname(__file__))


def image_to_base64(image_name):
    image_path = os.path.join(base_dir, "data", "images", image_name)
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()


def list_cv_data():
    cv_folder = os.path.join(base_dir, "data", "cv")
    return [os.path.join(cv_folder, folder, 'information.json') for folder in os.listdir(cv_folder)]


def templating(data, template_url):
    main_url = os.path.join(template_url, 'main.html')
    with open(main_url, 'r', encoding='utf-8') as g:
        template = jinja2.Template(g.read())
    return template.render(data)


def html_to_pdf(html_str):
    return pdfkit.from_string(html_str, False, options={'quiet': ''})


def main():
    template_url = os.path.join(base_dir, "data", "templates", "template1")
    cv_data = list_cv_data()
    images = {
        "github": image_to_base64("github.png"),
        "linkedin": image_to_base64("linkedin.png")
    }
    for cv_info_path in cv_data:
        with open(cv_info_path, 'r', encoding='utf-8') as f:
            cv_info = json.load(f)
            cv_info = {**cv_info, **images}
            cv_html = templating(cv_info, template_url)
            pdf_file = html_to_pdf(cv_html)
            dest = os.path.join(os.path.dirname(cv_info_path), 'cv.pdf')
        with open(dest, 'wb') as h:
            h.write(pdf_file)


if __name__ == '__main__':
    main()
