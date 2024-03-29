# build_project.py

import os
import json
import subprocess
import streamlit as st
from src.build_project import build_project


def add_entity_view():
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
    st.write("")
    st.write(":gray[All entities have an implicit `_id` field.]")
    st.markdown("---")
    if st.button("Go Back"):
        st.session_state['add_entity'] = False
        st.rerun()


def add_field_view(radio_selection):
    entity = st.session_state['entities'][radio_selection]
    st.header(f"{entity['name']} / {entity['name_plural']}")
    st.subheader("Add Field")
    with st.form(key="new_field_form"):
        field_name = st.text_input("Field Name")

        field_type = st.selectbox("Field Type",
                                  ["string", "int", "float", "boolean"] + list(st.session_state['entities'].keys()))
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


def entity_view(radio_selection):
    if st.session_state['entities']:
        entity = st.session_state['entities'][radio_selection]
        st.header(f"{entity['name']} / {entity['name_plural']}")
        st.markdown("<br>", unsafe_allow_html=True)
        if not entity['fields']:
            st.write(":gray[This entity has no fields yet.]")
            st.markdown("---")
        for field in entity['fields']:
            st.markdown(f"""
                    <div style="border:1px solid gray; padding:10px; margin:5px; border-radius:8px;">
                        <h4>{field['name']}: {field['type']}</h4>
                        <p>required: <strong>{field['is_required']}</strong>, unique: <strong>{field['is_unique']}</strong>, array: <strong>{field['is_array']}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Move Up", key=f"move_up_{field['name']}"):
                    index = st.session_state['entities'][radio_selection]['fields'].index(field)
                    if index > 0:
                        st.session_state['entities'][radio_selection]['fields'][index - 1], \
                        st.session_state['entities'][radio_selection]['fields'][index] = \
                            st.session_state['entities'][radio_selection]['fields'][index], \
                            st.session_state['entities'][radio_selection]['fields'][index - 1]
                        st.rerun()
            with col2:
                if st.button("Move Down", key=f"move_down_{field['name']}"):
                    index = st.session_state['entities'][radio_selection]['fields'].index(field)
                    if index < len(st.session_state['entities'][radio_selection]['fields']) - 1:
                        st.session_state['entities'][radio_selection]['fields'][index], \
                        st.session_state['entities'][radio_selection]['fields'][index + 1] = \
                            st.session_state['entities'][radio_selection]['fields'][index + 1], \
                            st.session_state['entities'][radio_selection]['fields'][index]
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
        st.write(":gray[No entities have been added yet.]")
        st.write(":gray[Click the button on the left to add one.]")


def dirty_shutdown():
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'streamlit.exe'], check=True)
        print("Streamlit process terminated.")
    except subprocess.CalledProcessError as e:
        print("Failed to terminate Streamlit process:", e)


def generate_json(dir_path):
    with open(os.path.join(dir_path, "db.json"), "w") as file:
        json.dump(list(st.session_state['entities'].values()), file, indent=2)
    st.success("Generated db.json!")
    st.balloons()


def start_build_project(option, output_dir):
    st.success(f"{option} API built!")
    st.balloons()
    option = {"REST": "rest", "GraphQL": "gql"}[option]
    build_project(option, output_dir)


def main():
    st.set_page_config(page_title="API Builder", page_icon=":rocket:", layout="centered")

    # State management for entities
    if 'entities' not in st.session_state:
        st.session_state['entities'] = {}
    if 'add_entity' not in st.session_state:
        st.session_state['add_entity'] = False
    if 'add_field' not in st.session_state:
        st.session_state['add_field'] = False
    if 'option' not in st.session_state:
        st.session_state['option'] = "REST"

    # Sidebar
    st.sidebar.title("Builder")
    radio_selection = st.sidebar.radio(
        "Entites" if st.session_state['entities'] else "No entities have been added yet.",
        st.session_state['entities'].keys() if st.session_state['entities'] else []
    )
    st.sidebar.markdown("")
    if st.sidebar.button("Add Entity"):
        st.session_state['add_entity'] = True
    st.sidebar.markdown("---")

    output_dir = st.sidebar.text_input("Output Directory")
    st.sidebar.button("Generate JSON", on_click=generate_json, args=[output_dir], disabled=not os.path.isdir(output_dir))
    st.sidebar.markdown("---")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.session_state['option'] = st.radio("API", ["REST", "GraphQL"])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(
            "Build Project",
            on_click=start_build_project,
            args=[st.session_state['option'], output_dir],
            disabled=not os.path.isfile(os.path.join(output_dir, "db.json"))
        )
    st.sidebar.markdown("---")

    st.sidebar.markdown("")
    st.sidebar.button("Shut Down", on_click=dirty_shutdown)

    # Main Page
    st.subheader(":rocket: Entity Builder")
    st.markdown("---")
    if st.session_state['add_entity']:
        add_entity_view()
    elif st.session_state['entities'] and st.session_state['add_field']:
        add_field_view(radio_selection)
    else:
        entity_view(radio_selection)


if __name__ == "__main__":
    main()
