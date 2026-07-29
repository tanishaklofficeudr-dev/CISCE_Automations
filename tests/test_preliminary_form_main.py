# python -m pytest tests\test_preliminary_form_main.py --headed -v 

import pytest
import allure

from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.school_details_page import SchoolDetailsPage
from pages.address_details_page import AddressDetailsPage
from pages.noc_details_page import NOCDetailsPage
from pages.trust_details_page import TrustDetailsPage
from pages.land_certificate_page import LandCertificatePage
from pages.upload_documents_page import UploadDocumentsPage

from utils.excel_reader import ExcelReader
from utils.logger import setup_logger
from utils.screenshot_util import ScreenshotUtil


excel = ExcelReader("test_data/Data_Schools.xlsx")
logger = setup_logger()

school_ids = excel.get_school_ids_to_execute()


@allure.epic("CISCE Preliminary Affiliation Form")
@allure.feature("End-to-End Form Submission")
@allure.severity(allure.severity_level.CRITICAL)
@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Preliminary Form")
@allure.sub_suite("Smoke")
@pytest.mark.smoke
@pytest.mark.e2e
@pytest.mark.preliminary_form
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.parametrize("school_id", school_ids)
def test_preliminary_form(page, school_id):
    allure.dynamic.title(f"Preliminary Form - {school_id}")
    allure.dynamic.description(
        f"End-to-End Regression & Sanity Test\n\n"
        f"School ID: {school_id}\n"
        f"Covers: Registration → Login → School Details → Address → NOC → "
        f"Trust Details → Land Certificate → Document Upload → Payment"
    )
    allure.dynamic.story("Complete Preliminary Form Submission")
    allure.dynamic.tag("smoke", "sanity", "regression", "e2e", "preliminary_form")
    logger.info(f"Starting execution for {school_id}")

    try:
        registration_data = excel.get_row_by_school_id(
            "Registration",
            school_id
        )

        login_data = excel.get_row_by_school_id(
            "Login",
            school_id
        )

        school_data = excel.get_row_by_school_id(
            "School_Details",
            school_id
        )

        address_data = excel.get_row_by_school_id(
            "Address_Details",
            school_id
        )

        noc_data = excel.get_row_by_school_id(
            "NOC_Details",
            school_id
        )

        trust_data = excel.get_row_by_school_id(
            "Trust_Details",
            school_id
        )


        land_data = excel.get_row_by_school_id(
            "Land_Certificate",
            school_id
        )

        upload_data = excel.get_row_by_school_id(
            "Upload_Documents",
            school_id
        )

        with allure.step("Registration"):
            RegistrationPage(page).register_school(registration_data)

        with allure.step("Login"):
            LoginPage(page).login(login_data)

        with allure.step("Click Next on Get Started page"):
            page.wait_for_url("**/preliminary/school/dashboard", timeout=6000)
            page.get_by_role("button", name="Next").click()

        with allure.step("Fill School Details"):
            SchoolDetailsPage(page).fill_school_details(school_data)

        with allure.step("Fill Address Details"):
            AddressDetailsPage(page).fill_address_details(address_data)

        with allure.step("Fill NOC Details"):
            NOCDetailsPage(page).fill_noc_details(noc_data)

        with allure.step("Fill Trust/Society Details"):
            TrustDetailsPage(page).fill_trust_details(trust_data)

        with allure.step("Fill Land Certificate Details"):
            LandCertificatePage(page).fill_land_details(land_data)

        with allure.step("Upload Documents & Payment"):
            UploadDocumentsPage(page).upload_documents(upload_data)

        logger.info(f"{school_id} executed successfully")
    
    except Exception as e:
        screenshot_path = ScreenshotUtil.take_screenshot(
            page,
            school_id
        )

        # Attach screenshot to allure report
        if screenshot_path:
            allure.attach.file(
                screenshot_path,
                name=f"Failure_{school_id}",
                attachment_type=allure.attachment_type.PNG
            )

        logger.error(f"Execution failed for {school_id}")
        logger.error(str(e))
        logger.error(f"Screenshot: {screenshot_path}")

        raise

        # page.get_by_role("button", name="Next").click()
