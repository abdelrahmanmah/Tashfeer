import streamlit as st
import math
import string
import re
import numpy as np

# --- Cipher Functions (Keep these exactly the same as the previous version) ---

# 1. Rail Fence Cipher
def rail_fence_encrypt(text, key):
    if not isinstance(key, int) or key < 2:
        return "Error: Rail Fence key must be an integer >= 2."
    if key >= len(text):
        st.warning(f"Rail Fence key ({key}) >= text length ({len(text)}). Result might be unexpected or just the original text.")
        key = len(text) if len(text) > 1 else 2 # Adjust key somewhat defensively
        if key < 2: key = 2 # Ensure key is at least 2

    rails = [''] * key
    direction = 1
    row = 0
    for char in text:
        rails[row] += char
        # Check prevents index error if key is 1 (though we try to prevent key < 2)
        if key > 1:
            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1
            row += direction
    return ''.join(rails)

def rail_fence_decrypt(ciphertext, key):
    if not isinstance(key, int) or key < 2:
        return "Error: Rail Fence key must be an integer >= 2."
    if not ciphertext:
        return "" # Handle empty input
    if key >= len(ciphertext):
         st.warning(f"Rail Fence key ({key}) >= ciphertext length ({len(ciphertext)}). Result might be unexpected.")
         key = len(ciphertext) if len(ciphertext) > 1 else 2 # Adjust defensively
         if key < 2: key = 2 # Ensure key is at least 2

    # Calculate rail lengths
    rail_lengths = [0] * key
    direction = 1
    row = 0
    # Simulate encryption path to find lengths
    if key <= 1: return ciphertext # Avoid infinite loop if adjusted key becomes <= 1
    temp_len = 0
    if key > 1: # Prevent index issues if key becomes 1 despite checks
        while temp_len < len(ciphertext):
            rail_lengths[row] += 1
            temp_len += 1
            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1
            row += direction
            # Break if stuck (e.g., key=1 scenario, though prevented above)
            if direction == 0 and key > 1: break # Avoid infinite loop for edge cases
    else: # If key somehow becomes 1 or less, assign all length to first rail
        if key > 0: rail_lengths[0] = len(ciphertext)


    # Build the rails from ciphertext
    rails = []
    current_pos = 0
    for length in rail_lengths:
        # Ensure rail has positive length before slicing
        if length > 0:
            rails.append(list(ciphertext[current_pos : current_pos + length]))
        else:
            rails.append([]) # Add empty list for rails with zero length
        current_pos += length

    # Read off the rails
    result = ''
    direction = 1
    row = 0
    rail_indices = [0] * key # Keep track of current index within each rail list

    # Simulate path again to reconstruct
    temp_len = 0
    if key <= 1: return ciphertext # Avoid infinite loop
    while temp_len < len(ciphertext):
        # Check if rail and index are valid before accessing
        if row < len(rails) and rail_indices[row] < len(rails[row]):
             result += rails[row][rail_indices[row]]
             rail_indices[row] += 1
        else:
             # This indicates a potential mismatch between calculated lengths and actual structure
             st.warning(f"Rail Fence Decryption: Index out of bounds for row {row}. Result may be incomplete.")
             break

        temp_len += 1
        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1
        # Only change row if key > 1
        if key > 1:
             row += direction
        # Break if stuck
        if direction == 0 and key > 1 : break

    return result

# 2. Row Transposition Cipher
def get_key_order(key):
    key = key.lower()
    sorted_key = sorted([(char, i) for i, char in enumerate(key)])
    order = [0] * len(key)
    for read_pos, (_, original_index) in enumerate(sorted_key):
        order[original_index] = read_pos
    return order

def row_transposition_encrypt(text, key):
    if not isinstance(key, str) or not key:
        return "Error: Row Transposition key must be a non-empty string."
    key_clean = re.sub(r'[^A-Za-z]', '', key).upper()
    if not key_clean:
        return "Error: Row Transposition key must contain letters."

    key_len = len(key_clean)
    text_len = len(text)
    num_rows = math.ceil(text_len / key_len)
    padded_len = num_rows * key_len
    padding_char = 'X'
    padded_text = text.ljust(padded_len, padding_char)

    grid = np.array(list(padded_text)).reshape(num_rows, key_len)
    read_order_map = get_key_order(key_clean)
    encrypted_text = ""
    for read_pos in range(key_len):
        original_col_index = -1
        for idx, pos in enumerate(read_order_map):
            if pos == read_pos:
                original_col_index = idx
                break
        if original_col_index != -1:
            encrypted_text += "".join(grid[:, original_col_index])
        else:
             return "Error: Column mapping failed during encryption."
    return encrypted_text

def row_transposition_decrypt(ciphertext, key):
    if not isinstance(key, str) or not key:
        return "Error: Row Transposition key must be a non-empty string."
    key_clean = re.sub(r'[^A-Za-z]', '', key).upper()
    if not key_clean:
        return "Error: Row Transposition key must contain letters."

    key_len = len(key_clean)
    text_len = len(ciphertext)
    if text_len == 0: return ""
    if key_len == 0: return "Error: Processed key is empty."

    num_rows = math.ceil(text_len / key_len) if key_len > 0 else 0 # Avoid division by zero
    if num_rows == 0 and text_len > 0: return "Error: Key length is zero but ciphertext exists." # Should be caught earlier

    num_full_cols = text_len % key_len if key_len > 0 and text_len % key_len != 0 else key_len
    num_short_cols = key_len - num_full_cols if key_len > 0 else 0

    read_order_map = get_key_order(key_clean)
    cols_by_read_order = sorted(range(key_len), key=lambda k: read_order_map[k])

    col_lengths = [0] * key_len
    for i, original_col_index in enumerate(cols_by_read_order):
        if i < num_full_cols:
            col_lengths[original_col_index] = num_rows
        else:
            col_lengths[original_col_index] = num_rows - 1 if num_rows > 0 else 0

    grid = [['' for _ in range(key_len)] for _ in range(num_rows)]
    current_pos = 0
    for read_pos in range(key_len):
        original_col_index = -1
        for idx, pos in enumerate(read_order_map):
            if pos == read_pos:
                original_col_index = idx
                break

        if original_col_index != -1:
            col_len = col_lengths[original_col_index]
            if current_pos + col_len > text_len:
                st.warning(f"Row Transposition Decryption: Mismatch detected filling column {original_col_index}. Result may be incorrect.")
                col_data = ciphertext[current_pos:]
                col_len = len(col_data)
            else:
                col_data = ciphertext[current_pos : current_pos + col_len]

            current_pos += col_len
            for row_index in range(col_len):
                 # Check if row_index is valid for the potentially smaller grid if num_rows is 0
                 if row_index < num_rows:
                     grid[row_index][original_col_index] = col_data[row_index]
        else:
            return "Error: Column mapping failed during decryption."

    decrypted_text = ""
    for row in grid:
        decrypted_text += "".join(row)

    padding_char = 'X'
    num_padded_chars = (num_rows * key_len) - text_len if key_len > 0 else 0
    if num_padded_chars > 0:
       if decrypted_text.endswith(padding_char * num_padded_chars):
           decrypted_text = decrypted_text[:-num_padded_chars]

    return decrypted_text


# 3. Caesar Cipher
def caesar_cipher(text, key, mode='encrypt'):
    if not isinstance(key, int):
        return "Error: Caesar key must be an integer."
    result = ""
    key = key % 26 # Ensure key is within 0-25 range
    if mode == 'decrypt':
        key = -key

    for char in text:
        if 'a' <= char <= 'z':
            shifted = ord('a') + (ord(char) - ord('a') + key) % 26
            result += chr(shifted)
        elif 'A' <= char <= 'Z':
            shifted = ord('A') + (ord(char) - ord('A') + key) % 26
            result += chr(shifted)
        else:
            result += char # Keep non-alphabetic characters as is
    return result

def caesar_encrypt(text, key):
    return caesar_cipher(text, key, mode='encrypt')

def caesar_decrypt(ciphertext, key):
    return caesar_cipher(ciphertext, key, mode='decrypt')

# 4. Vigenère Cipher
def vigenere_cipher(text, key, mode='encrypt'):
    if not isinstance(key, str) or not key:
        return "Error: Vigenere key must be a non-empty string."
    key_clean = re.sub(r'[^A-Za-z]', '', key).upper() # Keep only letters, uppercase
    if not key_clean:
        return "Error: Vigenere key must contain letters."

    result = ""
    key_index = 0
    key_len = len(key_clean)

    for char in text:
        if 'a' <= char <= 'z':
            key_char = key_clean[key_index % key_len]
            key_shift = ord(key_char) - ord('A')
            if mode == 'decrypt':
                key_shift = -key_shift

            shifted = ord('a') + (ord(char) - ord('a') + key_shift) % 26
            result += chr(shifted)
            key_index += 1 # Only advance key index for letters
        elif 'A' <= char <= 'Z':
            key_char = key_clean[key_index % key_len]
            key_shift = ord(key_char) - ord('A')
            if mode == 'decrypt':
                key_shift = -key_shift

            shifted = ord('A') + (ord(char) - ord('A') + key_shift) % 26
            result += chr(shifted)
            key_index += 1 # Only advance key index for letters
        else:
            result += char # Keep non-alphabetic characters as is
            # Do not advance key_index for non-letters

    return result

def vigenere_encrypt(text, key):
    return vigenere_cipher(text, key, mode='encrypt')

def vigenere_decrypt(ciphertext, key):
    return vigenere_cipher(ciphertext, key, mode='decrypt')

# --- Streamlit App ---

st.set_page_config(page_title="Tashfeer", page_icon="🕶️", layout="wide")

# --- Narrative Elements ---
title_icon = "🕶️"
encrypt_icon = "🔒"
decrypt_icon = "🔓"
transposition_icon = "🔀"
substitution_icon = "🔄"
combined_icon = "✨" # Or 🔒+🔀
key_icon = "🗝️"
message_icon = "📝"
output_icon = "📦"
execute_icon = "🚀"
success_icon = "✅"
error_icon = "🚨"
info_icon = "ℹ️"
warning_icon = "⚠️"

st.title(f"{title_icon} Welcome to Tashfeer! {title_icon}")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Control ⚙️")
operation = st.sidebar.radio(
    "Select Your Objective:",
    (f"{encrypt_icon} Encrypt", f"{decrypt_icon} Decrypt"),
    key="op"
)
current_op_verb = "Encrypting" if operation.startswith(encrypt_icon) else "Decrypting"
current_op_noun = "Encryption" if operation.startswith(encrypt_icon) else "Decryption"

st.sidebar.markdown("---")
st.sidebar.subheader("Cryptographic Approach:")
cipher_type = st.sidebar.radio(
    "Choose your strategy:",
    (f"{transposition_icon} Transposition Only (Rearrange)",
     f"{substitution_icon} Substitution Only (Swap Letters)",
     f"{combined_icon} Combined"),
    key="cipher_type",
    help="Combined Ops: Encrypt applies Sub then Trans. Decrypt applies Trans then Sub."
)
st.sidebar.markdown("---")

# --- Conditional Algorithm Selection ---
transposition_algo = None
transposition_key_input = None
substitution_algo = None
substitution_key_input = None
selected_trans_protocol = ""
selected_sub_protocol = ""

# Transposition Selection (if needed)
if cipher_type.startswith(transposition_icon) or cipher_type.startswith(combined_icon):
    st.sidebar.subheader(f"{transposition_icon} Transposition Protocol:")
    transposition_algo = st.sidebar.selectbox(
        "Select scrambling method:",
        ("🚧 Rail Fence (Zigzag)", "📊 Row Transposition (Grid Lock)"),
        key="trans_algo"
    )
    selected_trans_protocol = transposition_algo.split('(')[0].strip() # Get "Rail Fence" or "Row Transposition"

    # Get Transposition Key
    if transposition_algo.startswith("🚧"): # Rail Fence
        transposition_key_input = st.sidebar.number_input(
            f"{key_icon} Enter Rails Code (Number >= 2):",
            min_value=2, step=1, value=3, key="trans_key_rf",
            help="The number of 'rails' for the zigzag pattern."
        )
    elif transposition_algo.startswith("📊"): # Row Transposition
        transposition_key_input = st.sidebar.text_input(
            f"{key_icon} Enter Grid Keyword (Letters only):",
            value="SECRET", key="trans_key_row",
            help="Keyword determining the column read order (e.g., 'AGENT')."
        )
    st.sidebar.markdown("---")

# Substitution Selection (if needed)
if cipher_type.startswith(substitution_icon) or cipher_type.startswith(combined_icon):
    st.sidebar.subheader(f"{substitution_icon} Substitution Protocol:")
    substitution_algo = st.sidebar.selectbox(
        "Select letter-swapping technique:",
        ("🅰️ Caesar Shift (Simple)", "🔑 Vigenère Keyword (Poly-Shift)"),
        key="sub_algo"
    )
    selected_sub_protocol = substitution_algo.split('(')[0].strip() # Get "Caesar Shift" or "Vigenere Keyword"

    # Get Substitution Key
    if substitution_algo.startswith("🅰️"): # Caesar
        substitution_key_input = st.sidebar.number_input(
            f"{key_icon} Enter Shift Value (0-25):",
            min_value=0, max_value=25, step=1, value=3, key="sub_key_caesar",
            help="How many positions to shift each letter (e.g., 3 means A->D)."
        )
    elif substitution_algo.startswith("🔑"): # Vigenere
        substitution_key_input = st.sidebar.text_input(
            f"{key_icon} Enter Vigenère Codeword (Letters only):",
            value="KEY", key="sub_key_vig",
            help="The secret keyword used for multiple shifts (e.g., 'CIPHER')."
        )
    st.sidebar.markdown("---")


# --- Main Area Layout ---
col1, col2 = st.columns(2)

with col1:
    input_label = f"{message_icon} Input ({'Plaintext' if operation.startswith(encrypt_icon) else 'Ciphertext'}):"
    st.header(input_label)
    input_text = st.text_area(
        "Drop your message in the secure box:",
        height=250,
        placeholder="Type or paste the sensitive information here...",
        key="input_text"
    )

with col2:
    output_label = f"{output_icon} Output ({'Ciphertext' if operation.startswith(encrypt_icon) else 'Decoded Intel'}):"
    st.header(output_label)
    output_text_area = st.empty() # Placeholder for the output
    output_text_area.text_area(
        "Processed message will appear in this secure container:",
        height=250,
        value="",
        key="output_text",
        disabled=True # Make it read-only visually
    )

# --- Process Button and Logic ---
st.markdown("---") # Separator
if st.button(f"{execute_icon} Engage Cipher Engine! {execute_icon}", key="process_button"):

    # Re-fetch current operation state inside button click
    current_op_verb = "Encrypting" if operation.startswith(encrypt_icon) else "Decrypting"
    current_op_noun = "Encryption" if operation.startswith(encrypt_icon) else "Decryption"

    result = ""
    error_occurred = False
    error_message = ""
    status_updates = [] # Store messages for display

    # --- Input Validation ---
    status_updates.append(f"{info_icon} Checking mission parameters...")
    if not input_text:
        error_message = f"{error_icon} Critical Alert! No intel provided for {current_op_verb.lower()}."
        error_occurred = True

    # Validate keys ONLY IF the corresponding cipher type is selected
    transposition_key = transposition_key_input
    substitution_key = substitution_key_input

    if not error_occurred and (cipher_type.startswith(transposition_icon) or cipher_type.startswith(combined_icon)):
        status_updates.append(f"{info_icon} Verifying Transposition Protocol ({selected_trans_protocol})...")
        if transposition_algo.startswith("🚧"): # Rail Fence
            if not isinstance(transposition_key, int) or transposition_key < 2:
                error_message = f"{error_icon} Invalid Rails Code! Must be a number >= 2."
                error_occurred = True
        elif transposition_algo.startswith("📊"): # Row Transposition
             key_check = transposition_key if isinstance(transposition_key, str) else ""
             if not re.search('[a-zA-Z]', key_check):
                error_message = f"{error_icon} Invalid Grid Keyword! Must contain letters."
                error_occurred = True
        if not error_occurred: status_updates.append(f"{success_icon} Transposition parameters locked in.")


    if not error_occurred and (cipher_type.startswith(substitution_icon) or cipher_type.startswith(combined_icon)):
        status_updates.append(f"{info_icon} Verifying Substitution Protocol ({selected_sub_protocol})...")
        if substitution_algo.startswith("🅰️"): # Caesar
            # Allow 0 shift, technically valid though useless
             if not isinstance(substitution_key, int) or substitution_key < 0:
                 error_message = f"{error_icon} Invalid Shift Value! Must be a number >= 0."
                 error_occurred = True
        elif substitution_algo.startswith("🔑"): # Vigenere
             key_check = substitution_key if isinstance(substitution_key, str) else ""
             if not re.search('[a-zA-Z]', key_check):
                 error_message = f"{error_icon} Invalid Vigenère Codeword! Must contain letters."
                 error_occurred = True
        if not error_occurred: status_updates.append(f"{success_icon} Substitution parameters confirmed.")

    # --- Processing ---
    if error_occurred:
        st.error(error_message)
        output_text_area.text_area(
            "Processed message will appear in this secure container:",
            value=f"{error_icon} Mission Aborted due to parameter errors.",
            height=250, key="output_text_error", disabled=True
        )
        # Display status updates leading to error
        for msg in status_updates:
             if error_icon in msg or warning_icon in msg: st.error(msg)
             elif success_icon in msg: st.success(msg)
             else: st.info(msg)

    else:
        try:
            status_updates.append(f"{execute_icon} Initiating {current_op_noun} Sequence...")
            current_text = input_text
            final_result = ""

            # Define selected functions dynamically (only if needed)
            sub_encrypt_func = None
            sub_decrypt_func = None
            trans_encrypt_func = None
            trans_decrypt_func = None

            # Map selected protocols back to function names and keys
            if cipher_type.startswith(substitution_icon) or cipher_type.startswith(combined_icon):
                 sub_encrypt_func = caesar_encrypt if substitution_algo.startswith("🅰️") else vigenere_encrypt
                 sub_decrypt_func = caesar_decrypt if substitution_algo.startswith("🅰️") else vigenere_decrypt
            if cipher_type.startswith(transposition_icon) or cipher_type.startswith(combined_icon):
                 trans_encrypt_func = rail_fence_encrypt if transposition_algo.startswith("🚧") else row_transposition_encrypt
                 trans_decrypt_func = rail_fence_decrypt if transposition_algo.startswith("🚧") else row_transposition_decrypt

            # --- Execute Based on Cipher Type ---
            if operation.startswith(encrypt_icon): # Encrypt
                if cipher_type.startswith(substitution_icon): # Sub Only
                    status_updates.append(f"{info_icon} Applying {selected_sub_protocol} {current_op_noun}...")
                    final_result = sub_encrypt_func(current_text, substitution_key)
                elif cipher_type.startswith(transposition_icon): # Trans Only
                    status_updates.append(f"{info_icon} Applying {selected_trans_protocol} {current_op_noun}...")
                    final_result = trans_encrypt_func(current_text, transposition_key)
                elif cipher_type.startswith(combined_icon): # Combined
                    status_updates.append(f"{info_icon} Layer 1: Applying {selected_sub_protocol} {current_op_noun}...")
                    intermediate_text = sub_encrypt_func(current_text, substitution_key)
                    if "Error:" in intermediate_text: final_result = intermediate_text
                    else:
                         status_updates.append(f"{info_icon} Layer 2: Applying {selected_trans_protocol} {current_op_noun}...")
                         final_result = trans_encrypt_func(intermediate_text, transposition_key)

            elif operation.startswith(decrypt_icon): # Decrypt
                if cipher_type.startswith(substitution_icon): # Sub Only
                    status_updates.append(f"{info_icon} Applying {selected_sub_protocol} {current_op_noun}...")
                    final_result = sub_decrypt_func(current_text, substitution_key)
                elif cipher_type.startswith(transposition_icon): # Trans Only
                    status_updates.append(f"{info_icon} Applying {selected_trans_protocol} {current_op_noun}...")
                    final_result = trans_decrypt_func(current_text, transposition_key)
                elif cipher_type.startswith(combined_icon): # Combined (Reverse Order)
                    status_updates.append(f"{info_icon} Layer 1: Reversing {selected_trans_protocol} {current_op_noun}...")
                    intermediate_text = trans_decrypt_func(current_text, transposition_key)
                    if "Error:" in intermediate_text: final_result = intermediate_text
                    else:
                        status_updates.append(f"{info_icon} Layer 2: Reversing {selected_sub_protocol} {current_op_noun}...")
                        final_result = sub_decrypt_func(intermediate_text, substitution_key)

            # --- Display Status & Result ---
            for msg in status_updates:
                 if error_icon in msg or warning_icon in msg: st.error(msg)
                 elif success_icon in msg: st.success(msg)
                 else: st.info(msg)

            # Check final result for internal function errors
            if "Error:" in final_result:
                st.error(f"{error_icon} Protocol Failure during processing: {final_result}")
                output_text_area.text_area(
                    "Processed message will appear in this secure container:",
                    value=f"{error_icon} Failed: {final_result}",
                    height=250, key="output_text_proc_error", disabled=True
                )
            else:
                 # Success!
                output_text_area.text_area(
                    "Processed message will appear in this secure container:",
                    value=final_result,
                    height=250, key="output_text_filled", disabled=True
                )
                st.success(f"{success_icon} Mission Accomplished! {current_op_noun} Complete.")
                st.balloons()

        except Exception as e:
            st.error(f"{error_icon} Catastrophic System Failure! Contact HQ.")
            st.exception(e) # Show full traceback for debugging
            output_text_area.text_area(
                 "Processed message will appear in this secure container:",
                 value=f"{error_icon} An unexpected error stopped processing: {e}",
                 height=250, key="output_text_exception", disabled=True
            )
            # Display status leading up to crash
            for msg in status_updates:
                 if error_icon in msg or warning_icon in msg: st.error(msg)
                 elif success_icon in msg: st.success(msg)
                 else: st.info(msg)

# --- Explanations (Briefing Room) ---
st.markdown("---")
with st.expander(f"📖 Access Cipher Protocol Briefings..."):
    # Fetch current state again for accurate explanation
    current_op_verb_exp = "Encryption" if operation.startswith(encrypt_icon) else "Decryption"
    selected_approach = "Unknown"
    if cipher_type.startswith(transposition_icon): selected_approach = "Transposition Only"
    elif cipher_type.startswith(substitution_icon): selected_approach = "Substitution Only"
    elif cipher_type.startswith(combined_icon): selected_approach = "Combined Ops"

    st.markdown(f"""
    **Selected Operation:** {current_op_verb_exp}
    **Selected Approach:** {selected_approach}

    **Available Protocols:**

    *   **{transposition_icon} Transposition (Rearrangement):** Changes the *order* of letters.
        *   `🚧 Rail Fence`: Writes message in a zigzag, reads row by row. Needs *Rails Code* ({key_icon}).
        *   `📊 Row Transposition`: Uses a grid and *Grid Keyword* ({key_icon}) to scramble columns.
    *   **{substitution_icon} Substitution (Letter Swapping):** Changes the letters *themselves*.
        *   `🅰️ Caesar Shift`: Simple shift by a *Shift Value* ({key_icon}). Easy to break!
        *   `🔑 Vigenère Keyword`: Uses a *Codeword* ({key_icon}) for multiple shifts. Much stronger.

    **Execution Flow ({selected_approach}):**
    """)
    if cipher_type.startswith(combined_icon):
        st.markdown(f"""
        - **{encrypt_icon} Encryption:** Apply Substitution first, then Transposition to the result.
        - **{decrypt_icon} Decryption:** Apply Transposition reversal first, then Substitution reversal.
        """)
    elif cipher_type.startswith(transposition_icon):
         st.markdown(f"- **{encrypt_icon}/{decrypt_icon}:** Apply selected Transposition protocol only.")
    elif cipher_type.startswith(substitution_icon):
         st.markdown(f"- **{encrypt_icon}/{decrypt_icon}:** Apply selected Substitution protocol only.")


# --- Footer ---
st.markdown("---")
st.caption(f"{title_icon} Cipher HQ - For Your Eyes Only. This message will self-destruct... eventually.")
