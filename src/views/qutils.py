from PySide6.QtGui import QActionGroup

def bind_menu_to_actions(menu, actions, single_select = False, selected_index = 0, parent = None):
    action_group = QActionGroup(parent)
    action_group.setExclusive(single_select)

    for action in actions:
        action.setCheckable(True)
        action_group.addAction(action)
        menu.addAction(action)

    actions[selected_index].setChecked(True)

class WidgetDataUpdateMixin:
    def _update_gui_with_data(self):
        pass