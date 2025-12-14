import streamlit as st

# --- Konfiguracja i Inicjalizacja Stanu Sesji ---

st.set_page_config(page_title="System Zarządzania Magazynem", layout="centered")

# Inicjalizacja magazynu w st.session_state.
# Używamy słownika: {nazwa_towaru (str): liczba_sztuk (int)}
if 'magazyn' not in st.session_state:
    st.session_state['magazyn'] = {
        "Laptop": 10,
        "Monitor": 5,
        "Klawiatura": 25
    }

# --- Funkcje Logiki Magazynowej ---

def dodaj_lub_zaktualizuj_towar():
    """Dodaje nowy towar lub zwiększa ilość istniejącego."""
    
    # Pobieranie wartości z widgetów input (używając ich kluczy)
    nazwa_towaru = st.session_state.nazwa_towaru_input.strip()
    ilosc = st.session_state.ilosc_input

    if not nazwa_towaru:
        st.error("Nazwa towaru jest wymagana.")
        return

    # Walidacja ilości (Streamlit number_input powinien to zapewnić, ale warto sprawdzić)
    if not isinstance(ilosc, int) or ilosc <= 0:
        st.error("Ilość musi być dodatnią liczbą całkowitą.")
        return

    # Logika dodawania/aktualizacji
    if nazwa_towaru in st.session_state['magazyn']:
        # Aktualizacja ilości
        st.session_state['magazyn'][nazwa_towaru] += ilosc
        st.success(f"Zaktualizowano: Dodano **{ilosc}** sztuk towaru '{nazwa_towaru}'. Nowy zapas: {st.session_state['magazyn'][nazwa_towaru]} szt.")
    else:
        # Dodanie nowego towaru
        st.session_state['magazyn'][nazwa_towaru] = ilosc
        st.success(f"Dodano nowy towar: '**{nazwa_towaru}**' w ilości **{ilosc}** sztuk.")

    # Wyczyszczenie pola tekstowego po submicie (dla lepszego UX)
    st.session_state.nazwa_towaru_input = ""
    st.session_state.ilosc_input = 1 # Reset do domyślnej wartości 1


def usun_towar(nazwa_towaru):
    """Usuwa towar z listy magazynowej po nazwie."""
    if nazwa_towaru in st.session_state['magazyn']:
        del st.session_state['magazyn'][nazwa_towaru]
        st.success(f"Usunięto towar '{nazwa_towaru}' z magazynu.")

# --- Interfejs Użytkownika Streamlit ---

st.title("📦 System Zarządzania Magazynem")
st.markdown("---")

# Sekcja Dodawania Towaru
st.subheader("➕ Dodaj lub Zaktualizuj Zapas")

# Użycie st.form do grupowania inputów i użycia pojedynczego przycisku submit
with st.form("dodaj_formularz", clear_on_submit=False):
    # Dzielimy formularz na kolumny
    col_name, col_qty = st.columns([0.7, 0.3])

    with col_name:
        st.text_input(
            "Nazwa Towaru:",
            key='nazwa_towaru_input',
            placeholder="Wprowadź nazwę produktu"
        )
    
    with col_qty:
        st.number_input(
            "Ilość Sztuk:",
            min_value=1,
            step=1,
            value=1,
            key='ilosc_input'
        )
    
    # Przycisk submit formularza
    st.form_submit_button(
        "Zapisz w Magazynie",
        on_click=dodaj_lub_zaktualizuj_towar,
        type="primary"
    )

st.markdown("---")

# Sekcja Wyświetlania Magazynu
st.subheader("Aktualny Stan Magazynu")

magazyn_items = st.session_state['magazyn']

if magazyn_items:
    st.markdown(f"**Liczba unikalnych produktów:** **{len(magazyn_items)}**")
    st.markdown("")

    # Tworzenie nagłówków tabeli/listy za pomocą kolumn
    header_col1, header_col2, header_col3 = st.columns([0.6, 0.2, 0.2])
    header_col1.markdown("**Nazwa Towaru**")
    header_col2.markdown("**Ilość (szt.)**")
    
    for nazwa, ilosc in magazyn_items.items():
        # Tworzenie rzędu dla każdego produktu
        row_col1, row_col2, row_col3 = st.columns([0.6, 0.2, 0.2])
        
        with row_col1:
            st.write(nazwa)
        
        with row_col2:
            st.write(ilosc)
            
        with row_col3:
            # Przycisk usuwania z unikalnym kluczem i funkcją on_click
            st.button(
                "Usuń",
                key=f"usun_{nazwa}",
                on_click=usun_towar,
                args=(nazwa,), 
                help=f"Trwale usuń '{nazwa}' z magazynu."
            )
else:
    st.info("Magazyn jest pusty. Użyj formularza 'Dodaj lub Zaktualizuj Zapas' powyżej, aby rozpocząć.")
