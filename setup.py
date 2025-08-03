from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="frappe_whatsapp_login",
    version="0.0.1",
    description="WhatsApp OTP-based login for Frappe/ERPNext",
    author="Leet IT Solutions",
    author_email="aman@leetitsolutions.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "frappe>=14.0.0",  # Adjust to your version
        "requests>=2.25.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Frappe",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
