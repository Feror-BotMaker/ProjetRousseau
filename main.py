from playwright.sync_api import Playwright, sync_playwright, expect
from pygrammalecte import grammalecte_text
from time import sleep
from random import randint

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.projet-voltaire.fr/voltaire/com.woonoz.gwt.woonoz.Voltaire/Voltaire.html?returnUrl=www.projet-voltaire.fr/choix-parcours/&applicationCode=pv")
    input("Entrez vos identifiants dans le navigateur, puis appuyez sur Entrée ici pour continuer...")
    input("Rendez-vous dans le module orthographe, lancez un exercice, puis appuyez sur Entrée ici pour continuer...")
    while True:
        try:
            page.query_selector(".dialogLeftButton.secondaryButton").click()
        except:
            print("")
        try:
            page.get_by_text("LA PROCHAINE QUESTION PORTERA SUR")
            sleep(2)
            page.query_selector(".understoodButton").click()
            sleep(3)
            # Les 3 phrases sont apparues
            while True:
                les3Phrases = page.query_selector_all(".intensiveQuestion")
                for phrase in les3Phrases:
                    if len(list(grammalecte_text(phrase.query_selector(".sentence").inner_text()))):
                        phrase.query_selector(".buttonKo").click()
                    else:
                        phrase.query_selector(".buttonOk").click()
                sleep(0.5)
                try:
                    page.query_selector(".exitButton.primaryButton").click()
                    sleep(randint(1, 3))
                    break
                except:
                    page.query_selector(".retryButton.primaryButton").click()
                    sleep(randint(1, 3))
        except:
            phrase = page.query_selector(".question").inner_text()
            print(phrase)
            for message in grammalecte_text(phrase):
                print(phrase[message.start:message.end], message.message)
                try:
                    page.get_by_text(phrase[message.start:message.end]).click()
                    break
                except:
                    pass
            else:
                page.get_by_role("button", name="Il n'y a pas de faute").click()
            sleep(randint(1, 3))
            page.get_by_role("button", name="Suivant").click()
            sleep(randint(1, 3))
            '''page.get_by_text("arrivait").click()
            page.get_by_role("button", name="Suivant").click()
            page.get_by_text("peut").click()'''

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
