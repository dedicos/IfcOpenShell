from bpy.types import Panel
from blenderbim.bim.ifc import IfcStore
from ifcopenshell.api.type.data import Data


class BIM_PT_type(Panel):
    bl_label = "IFC Construction Type"
    bl_idname = "BIM_PT_type"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        props = context.active_object.BIMObjectProperties
        if not props.ifc_definition_id:
            return False
        if not IfcStore.get_element(props.ifc_definition_id):
            return False
        if props.ifc_definition_id not in Data.products and props.ifc_definition_id not in Data.types:
            Data.load(IfcStore.get_file(), props.ifc_definition_id)
        if props.ifc_definition_id not in Data.products and props.ifc_definition_id not in Data.types:
            return False
        if not Data.products.get(props.ifc_definition_id, None) and not Data.types.get(props.ifc_definition_id, None):
            return False
        return True

    def draw(self, context):
        oprops = context.active_object.BIMObjectProperties

        if oprops.ifc_definition_id in Data.products:
            self.draw_product_ui(context)
        else:
            self.draw_type_ui(context)

    def draw_type_ui(self, context):
        props = context.active_object.BIMTypeProperties
        oprops = context.active_object.BIMObjectProperties
        row = self.layout.row(align=True)
        row.label(text=f"{len(Data.types[oprops.ifc_definition_id])} Typed Objects")
        row.operator("bim.select_type_objects", icon="RESTRICT_SELECT_OFF", text="")

    def draw_product_ui(self, context):
        props = context.active_object.BIMTypeProperties
        oprops = context.active_object.BIMObjectProperties

        if props.is_editing_type:
            row = self.layout.row(align=True)

            row.prop(props, "relating_type_class", text="")
            if props.relating_type:
                row.prop(props, "relating_type", text="")
                row.operator("bim.assign_type", icon="CHECKMARK", text="")
            else:
                row.prop(props, "blank_relating_type", text="")
            row.operator("bim.disable_editing_type", icon="X", text="")
        else:
            row = self.layout.row(align=True)
            name = "{}/{}".format(
                Data.products[oprops.ifc_definition_id]["type"], Data.products[oprops.ifc_definition_id]["Name"]
            )
            if name == "None/None":
                label = "This object has no type"
            else:
                label = name
            row.label(text=label)
            row.operator("bim.select_similar_type", icon="RESTRICT_SELECT_OFF", text="")
            row.operator("bim.enable_editing_type", icon="GREASEPENCIL", text="")
            if name != "None/None":
                row.operator("bim.unassign_type", icon="X", text="")


def add_object_button(self, context):
    self.layout.operator("bim.add_type_instance", icon="PLUGIN")
