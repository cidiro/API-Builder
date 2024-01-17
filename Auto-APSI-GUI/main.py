import os
import sys
import json
import subprocess
import streamlit as st


# Dirty shut down of Streamlit process
def dirty_shut_down():
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'streamlit.exe'], check=True)
        print("Streamlit process terminated.")
    except subprocess.CalledProcessError as e:
        print("Failed to terminate Streamlit process:", e)


# Save entities to JSON file
def generate_json(dir_path):
    with open(os.path.join(dir_path, "db.json"), "w") as file:
        json.dump(list(st.session_state['entities'].values()), file, indent=2)
    st.success("Generated db.json!")
    st.balloons()
    dirty_shut_down()


# Main UI function
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: streamlit run main.py <target_directory>")
        sys.exit(1)

    st.set_page_config(page_title="Auto-APSI Builder", page_icon=":rocket:", layout="centered")

    # State management for entities
    if 'entities' not in st.session_state:
        st.session_state['entities'] = {}
    if 'add_entity' not in st.session_state:
        st.session_state['add_entity'] = False
    if 'add_field' not in st.session_state:
        st.session_state['add_field'] = False

    # Sidebar
    st.sidebar.title("Builder")
    radio_selection = st.sidebar.radio(
        "Entites" if st.session_state['entities'] else "No entities have been added yet.",
        st.session_state['entities'].keys() if st.session_state['entities'] else []
    )

    if st.sidebar.button("Add Entity"):
        st.session_state['add_entity'] = True

    st.sidebar.markdown("---")
    st.sidebar.button("Generate", on_click=generate_json, args=[sys.argv[1]])

    # Main Page
    st.subheader(":rocket: Entity Builder")
    st.markdown("---")

    if st.session_state['add_entity']:
        st.subheader("Create New Entity")
        with st.form(key="new_entity_form"):
            entity_name = st.text_input("Entity Name")
            entity_name_plural = st.text_input("Entity Name (Plural)")
            if st.form_submit_button("Save Entity"):
                st.session_state['entities'][entity_name] = {
                    "name": entity_name,
                    "name_plural": entity_name_plural,
                    "fields": []
                }
                st.session_state['add_entity'] = False
                st.rerun()
        st.markdown("---")
        if st.button("Go Back"):
            st.session_state['add_entity'] = False
            st.rerun()
    elif st.session_state['entities'] and st.session_state['add_field']:
        entity = st.session_state['entities'][radio_selection]
        st.header(f"{entity['name']} / {entity['name_plural']}")
        st.subheader("Add Field")
        with st.form(key="new_field_form"):
            field_name = st.text_input("Field Name")

            field_type = st.selectbox("Field Type", ["string", "int", "float", "boolean"] + list(st.session_state['entities'].keys()))
            field_is_required = st.checkbox("Required", value=True)
            field_is_unique = st.checkbox("Unique")
            field_is_array = st.checkbox("Array")
            if st.form_submit_button("Save Field"):
                st.session_state['entities'][radio_selection]['fields'].append({
                    "name": field_name,
                    "type": field_type,
                    "is_array": field_is_array,
                    "is_required": field_is_required,
                    "is_unique": field_is_unique
                })
                st.session_state['add_field'] = False
                st.rerun()
        st.markdown("---")
        if st.button("Go Back"):
            st.session_state['add_field'] = False
            st.rerun()
    elif st.session_state['entities']:
        entity = st.session_state['entities'][radio_selection]
        st.header(f"{entity['name']} / {entity['name_plural']}")
        if not entity['fields']:
            st.write("This entity has no fields yet.")
        for field in entity['fields']:
            st.markdown(f"""
                <div style="border:1px solid gray; padding:10px; margin:5px; border-radius:8px;">
                    <h4>{field['name']}: {field['type']}</h4>
                    <p>required: <strong>{field['is_required']}</strong>, unique: <strong>{field['is_unique']}</strong>, array: <strong>{field['is_array']}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Move Up", key=f"move_up_{field['name']}"):
                    index = st.session_state['entities'][radio_selection]['fields'].index(field)
                    if index > 0:
                        st.session_state['entities'][radio_selection]['fields'][index - 1], st.session_state['entities'][radio_selection]['fields'][index] = \
                            st.session_state['entities'][radio_selection]['fields'][index], st.session_state['entities'][radio_selection]['fields'][index - 1]
                        st.rerun()
            with col2:
                if st.button("Move Down", key=f"move_down_{field['name']}"):
                    index = st.session_state['entities'][radio_selection]['fields'].index(field)
                    if index < len(st.session_state['entities'][radio_selection]['fields']) - 1:
                        st.session_state['entities'][radio_selection]['fields'][index], st.session_state['entities'][radio_selection]['fields'][index + 1] = \
                            st.session_state['entities'][radio_selection]['fields'][index + 1], st.session_state['entities'][radio_selection]['fields'][index]
                        st.rerun()
            with col3:
                if st.button("Delete", key=f"delete_{field['name']}"):
                    st.session_state['entities'][radio_selection]['fields'].remove(field)
                    st.rerun()
        st.markdown("---")
        if st.button("Add Field"):
            st.session_state['add_field'] = True
            st.rerun()
    else:
        st.write("No entities have been added yet.\n\n"
                 "Click the button on the left to add one.")
