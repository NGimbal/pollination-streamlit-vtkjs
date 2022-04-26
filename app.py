import os
from typing import Dict

import streamlit as st
from streamlit_vtkjs import st_vtkjs

VIEWS = [
          '',
          'Top',
          'Bottom',
          'Left',
          'Right',
          'Front',
          'Back'
        ]

COLORSETS = [
    "Ladybug",
    "Nuanced Ladybug",
    "Multi-colored Ladybug",
    "Ecotect",
    "View Study",
    "Shadow Study",
    "Glare Study",
    "Annual Comfort",
    "Thermal Comfort",
    "Peak Load Balance",
    "Heat Sensation",
    "Cold Sensation",
    "Benefit/Harm",
    "Harm",
    "Benefit",
    "Shade Benefit/Harm",
    "Shade Harm",
    "Shade Benefit",
    "Energy Balance",
    "Energy Balance w/ Storage",
    "THERM",
    "Cloud Cover",
    "Black to White",
    "Blue, Green, Red",
    "Multicolored 2",
    "Multicolored 3",
    "Cool to Warm",
    "Viridis",
    "Spectral Low Blue"
]

st.set_page_config(page_title="Viewer Sample", layout="wide")

st.title("VTKJS in Streamlit!")

# branding, api-key and url
# we should wrap this up as part of the pollination-streamlit library
st.sidebar.image(
    'https://uploads-ssl.webflow.com/6035339e9bb6445b8e5f77d7/616da00b76225ec0e4d975ba_pollination_brandmark-p-500.png',
    use_column_width=True
)

if 'action_stack' not in st.session_state:
  st.session_state['action_stack'] = []

st.sidebar.header("VTKJS Viewer Controls")
sidebar_content = st.sidebar.empty()

_file = st.file_uploader(
    label=".vtkjs scene uploader",
    type=["vtkjs", "vtk", "vtp"],
    help="Upload a .vtkjs scene file"
)

content = _file.getvalue() if _file else None

vtkjs_container = st.empty()
vtkjs = None

def filter_by_name (name: str, array: list):
  if array is None or len(array) < 1:
    return None
  for item in array:
    if item['id'] == name:
      return item
  return None

def handle_bgcolor ():
  if 'bg_color' in st.session_state:
    hex = st.session_state.bg_color.lstrip('#')
    rgb = list(float(int(hex[i:i+2], 16) / 256) for i in (0, 2, 4))
    rgb.append(1)
    st.session_state.action_stack.append({
      'type': 'background-1',
      'value': rgb,
    })

def handle_views ():
  if 'view_select' in st.session_state:
    st.session_state.action_stack.append({
      'type': 'select-view',
      'value': st.session_state.view_select.lower(),
    })

def handle_colorset ():
  if 'colorset_select' in st.session_state:
    st.session_state.action_stack.append({
      'type': 'color-set',
      'value': st.session_state.colorset_select,
    })

def handle_toggleortho ():
  if 'toggle_ortho' in st.session_state:
    st.session_state.action_stack.append({
      'type': 'toggle-ortho',
      'value': st.session_state.toggle_ortho,
    })

def handle_isolatedata ():
  if 'isolate_data' in st.session_state:
    st.session_state.action_stack.append({
      'type': 'isolate-data',
      'value': st.session_state.isolate_data,
    })

def handle_resetcamera ():
  st.session_state.action_stack.append({
    'type': 'reset-camera',
  })

def handle_screenshot ():
  st.session_state.action_stack.append({
    'type': 'streamlit-screenshot',
  })

def handle_legendlabel ():
  st.session_state.action_stack.append({
    'type': 'legend-label',
    'value': st.session_state.legend_label,
  })

def handle_gimbalsize ():
  st.session_state.action_stack.append({
    'type': 'adjust-gimbal',
    'value': st.session_state.gimbal_size,
  })

def handle_visibility (item_id: str) :
  if item_id + '_vis' in st.session_state:
    st.session_state.action_stack.append({ 
      'type': 'visibility', 
      'ids': [item_id], 
      'value': st.session_state[item_id + '_vis'] 
    })

col1, col2, col3 = st.columns(3)
with col1.container():
  st.subheader("Viewer Arguments")
  toolbar = st.checkbox('Toolbar', value=True, key='toolbar_toggle', help='Show/Hide the toolbar.')
  sidebar = st.checkbox('Sidebar', value=True, key='sidebar_toggle', help='Show/Hide the side toolbar.')
  subscribe = st.checkbox('Subscribe', value=False, key='subscribe_toggle', help='Toggles whether the viewer will return its state to Streamlit or not.')
  clear = st.checkbox('Clear', value=True, key='clear_toggle', help='Toggles clearing the viewer when loading a new model.')

with vtkjs_container:
  vtkjs = st_vtkjs(
          "foobar",
          content=content,
          toolbar=st.session_state.toolbar_toggle,
          sidebar=st.session_state.sidebar_toggle,
          subscribe=st.session_state.subscribe_toggle,
          clear=st.session_state.clear_toggle,
          action_stack=st.session_state.action_stack,
          style={
              "height": "400px",
          },
        )

# action_stack is cleared after it's passed to the viewer
st.session_state.action_stack.clear()

# demonstrates how to keep streamlit state in sync with the viewer
bgcolor = '#ffffff'
if vtkjs is not None:
  if 'renderer' in vtkjs:
    if 'background' in vtkjs['renderer']:
      bgcolor = '#' + ''.join(['{:02x}'.format(int(x * 255)) for x in vtkjs['renderer']['background'][:3]])

with sidebar_content:
  with st.container():
    st.subheader('Global Controls')
    st.selectbox('View', VIEWS, key='view_select', on_change=handle_views)
    st.selectbox('Color sets', COLORSETS, key='colorset_select', on_change=handle_colorset)
    st.text_input('Legend Label', value="", key='legend_label', on_change=handle_legendlabel)
    st.number_input('Orienation Indicator Size', min_value=0.0, max_value=1.0, value=0.15, step=0.01, key='gimbal_size', on_change=handle_gimbalsize)
    st.color_picker("Background color", key='bg_color', value=bgcolor, on_change=handle_bgcolor)
    st.checkbox('Toggle perspective / orthographic', value=False, key='toggle_ortho', on_change=handle_toggleortho)
    st.checkbox('Isolate data', value=True, key='isolate_data', on_change=handle_isolatedata)
    st.button('Reset camera', key='reset-camera', on_click=handle_resetcamera)
    st.button('Screenshot', key='streamlit-screenshot', on_click=handle_screenshot)
    
    st.subheader('Scene Item Controls')
    with st.expander('VTKJS Scene'):
      if vtkjs is not None and 'scene' in vtkjs and len(vtkjs['scene']) > 0:
        for item in vtkjs['scene']:
          st.subheader(item['name'])
          st.checkbox('Show', 
            value=item['state']['visibility'], 
            key=item['id'] + '_vis', 
            kwargs={'item_id': item['id']}, 
            on_change=handle_visibility)

with col2.container():
  st.subheader("Component Value")
  if vtkjs is not None:
    st.json(vtkjs)