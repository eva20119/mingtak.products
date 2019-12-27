# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s mingtak.products -t test_product.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src mingtak.products.testing.MINGTAK_PRODUCTS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_product.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Product
  Given a logged-in site administrator
    and an add product form
   When I type 'My Product' into the title field
    and I submit the form
   Then a product with the title 'My Product' has been created

Scenario: As a site administrator I can view a Product
  Given a logged-in site administrator
    and a product 'My Product'
   When I go to the product view
   Then I can see the product title 'My Product'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add product form
  Go To  ${PLONE_URL}/++add++Product

a product 'My Product'
  Create content  type=Product  id=my-product  title=My Product


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the product view
  Go To  ${PLONE_URL}/my-product
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a product with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the product title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
