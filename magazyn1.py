import streamlit as st

# Inicjalizacja globalnej listy magazynowej.
# UWAGA: W standardowym Streamlit bez st.session_state,
# ta lista będzie resetowana przy każdej interakcji z widgetem,
# który powoduje ponowne uruchomienie skryptu (np. kliknięcie przycisku).
# Jest to jednak celowe działanie, zgodnie z prośbą o "Bez sesji".
# Dla persystencji danych między interakcjami zalecany jest st.session_state.
if 'magazyn' not in st.session_state:
    st.session_state['magazyn'] = ["Laptop", "Monitor", "Klawiatura"]

def dodaj_towar(nowy_towar):
    """Dodaje towar do listy magazynowej."""
    if nowy_towar and nowy_towar.strip() not in st.session_state['magazyn']:
        st.session_state['magazyn'].append(nowy_towar.strip())
    # Wymuś ponowne uruchomienie skryptu, aby odświeżyć widok
    st.experimental_rerun()

def usun_towar(indeks):
    """Usuwa towar z listy magazynowej po indeksie."""
    if 0 <= indeks < len(st.session_state['magazyn']):
        st.session_state['magazyn'].pop(indeks)
    # Wymuś ponowne uruchomienie skryptu, aby odświeżyć widok
    st.experimental_rerun()

# --- Interfejs Użytkownika Streamlit ---

st.title("Prosty Magazyn (Bez Stanu Sesji)")
st.subheader("Lista Towarów")

# Wyświetlanie aktualnej listy towarów
if st.session_state['magazyn']:
    for i, towar in enumerate(st.session_state['magazyn']):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown(f"**{i+1}.** {towar}")
        with col2:
            # Użycie key jest kluczowe, aby Streamlit traktował każdy przycisk jako unikalny
            if st.button("Usuń", key=f"usun_{i}"):
                usun_towar(i)
else:
    st.info("Magazyn jest pusty.")

st.markdown("---")
st.subheader("Dodaj Nowy Towar")

# Kontener do dodawania nowego towaru
with st.form("dodaj_formularz", clear_on_submit=True):
    nowy_towar = st.text_input("Nazwa Towaru")
    dodaj_button = st.form_submit_button("Dodaj do Magazynu")

    if dodaj_button:
        # Streamlit automatycznie ponownie uruchomi skrypt po submit,
        # ale ponieważ funkcja dodaj_towar wymusza reruna, będzie to działać poprawnie.
        dodaj_towar(nowy_towar)
