# FAKER - OSINT, SCRIPTING
Dette var en ganske interessant programmeringsoppgave i kvalifiseringsrunden for Cyberlandslaget med likhet til [cs50s egen oppgave](https://cs50.harvard.edu/college/2021/fall/psets/6/credit/). 
I tillegg var dette også en av de vanskeligere oppgavene i runden (en av de mest uløste).

## Oppgave beskrivelse av Unblvr
The feared, international hacker group L337RUs claims to have hacked a Norwegian online store and has leaked all the user data from it - complete with credit card (CC) and payment information (KID numbers)! However, we suspect the data is faked, and that the only valid account in their leak was used by one of the hackers themselves during the attack.

Help us figure out which account is the real one! It should be the only one where all the data fields are valid. I would normally ask my hacker friend for help with this, but all he said was 'Luhn'.

To help you get started, I wrote the parsing part of the script for you already. When you find the correct one, the script should print it for you. If you prefer doing it yourself, then enter the hacker's user id as the flag like this `flag{123456}`

## Løsning
Ut ifra beskrivelsen, var "Luhn" nevnt. Dette er faktisk blant de algoritmene som brukes for å bekrefte eller verifisere at et kredittkortnummer er gyldig. 
Mer om Luhn-algoritmen finner du [her](https://en.wikipedia.org/wiki/Luhn_algorithm). Vi laster ned filene og finner filen `faker_solve.py`. 
```python
def valid_credit_card_number(credit_card_number):
    # TODO write your code here
    return False

def valid_kid_number(kid_number):
    # TODO write your code here
    return False
```
Her må vi altså implementere Luhn algoritmen. Hovedideen er å ta vekk det siste sifferet i nummeret som skal sjekkes mot uttrykket `(10 - checksum mod 10) mod 10`, der`checksum` er beregnet ved å ta
de gjenværende sifrene og fra det første sifferet til høyre skal vi annenhver gang gange med 2 og plusse sifrene. I tilfellet sifferet blir større enn 9, må vi plusse sifrene sammen igjen.
Implementasjonen blir
```python
def sumdigits(sum):
    result = 0
    for i in str(sum): result += int(i)
    return result

def valid_credit_card_number(credit_card_number):
    givencd = int(str(credit_card_number)[-1])
    length = len(str(credit_card_number))
    checksum = 0
    for i in range(2, length + 1, 1):
        if i % 2 == 0: checksum += sumdigits(2*int(str(credit_card_number)[-1*i]))
        else: checksum += int(str(credit_card_number)[-1*i])
    if (10 - (checksum % 10)) % 10 == givencd: return True
    else: return False

def valid_kid_number(kid_number):
    givencd = int(str(kid_number)[-1])
    length = len(str(kid_number))
    checksum = 0
    for i in range(2, length + 1, 1):
        if i % 2 == 0: checksum += sumdigits(2*int(str(kid_number)[-1*i]))
        else: checksum += int(str(kid_number)[-1*i])
    if (10 - (checksum % 10)) % 10 == givencd: return True
    else: return False
 ```
Vi brukte `range(2, length + 1, 1)` siden vi har "droppet" det siste sifferet og skal begynne fra høyre ved å ta `str(credit_card_number)[-1*i]`.
Vi kjører programmet på terminalen og får id-en, dermed flagget:
```console
(base) stange@ericjoshua faker % python3 faker_solve.py
The hacker must be John Meadows!
The flag is flag{19872}
```
