<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="0" minScale="0" simplifyLocal="1" maxScale="0" simplifyAlgorithm="0" labelsEnabled="0" simplifyMaxScale="1" simplifyDrawingTol="1" readOnly="0" version="3.0.0-Girona" hasScaleBasedVisibilityFlag="0">
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol clip_to_extent="1" type="marker" name="0" alpha="1">
        <layer pass="0" locked="0" enabled="1" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="135,126,227,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="star" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="area" k="scale_method"/>
          <prop v="5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory width="15" penColor="#000000" labelPlacementMethod="XHeight" enabled="0" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" maxScaleDenominator="1e+8" backgroundAlpha="255" diagramOrientation="Up" lineSizeType="MM" rotationOffset="0" barWidth="5" penWidth="0" scaleBasedVisibility="0" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" height="15" minScaleDenominator="0" penAlpha="255" opacity="1" sizeType="MM">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" obstacle="0" placement="0" priority="0" zIndex="0" linePlacementFlags="2" dist="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option type="Map" name="properties">
          <Option type="Map" name="positionX">
            <Option type="bool" name="active" value="true"/>
            <Option type="QString" name="field" value="ID"/>
            <Option type="int" name="type" value="2"/>
          </Option>
          <Option type="Map" name="positionY">
            <Option type="bool" name="active" value="true"/>
            <Option type="QString" name="field" value="ID"/>
            <Option type="int" name="type" value="2"/>
          </Option>
          <Option type="Map" name="show">
            <Option type="bool" name="active" value="true"/>
            <Option type="QString" name="field" value="ID"/>
            <Option type="int" name="type" value="2"/>
          </Option>
        </Option>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="ID">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Elevation">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="InitLevel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MinLevel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MaxLevel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Diameter">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MinVolume">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="VolumeCurv">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="ID" index="0" name=""/>
    <alias field="Elevation" index="1" name=""/>
    <alias field="InitLevel" index="2" name=""/>
    <alias field="MinLevel" index="3" name=""/>
    <alias field="MaxLevel" index="4" name=""/>
    <alias field="Diameter" index="5" name=""/>
    <alias field="MinVolume" index="6" name=""/>
    <alias field="VolumeCurv" index="7" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ID" expression="" applyOnUpdate="0"/>
    <default field="Elevation" expression="0" applyOnUpdate="0"/>
    <default field="InitLevel" expression="10" applyOnUpdate="0"/>
    <default field="MinLevel" expression="0" applyOnUpdate="0"/>
    <default field="MaxLevel" expression="20" applyOnUpdate="0"/>
    <default field="Diameter" expression="50" applyOnUpdate="0"/>
    <default field="MinVolume" expression="0" applyOnUpdate="0"/>
    <default field="VolumeCurv" expression="''" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint constraints="1" field="ID" notnull_strength="2" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="Elevation" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="InitLevel" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="MinLevel" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="MaxLevel" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="Diameter" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="MinVolume" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="VolumeCurv" notnull_strength="0" exp_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="ID"/>
    <constraint exp="" desc="" field="Elevation"/>
    <constraint exp="" desc="" field="InitLevel"/>
    <constraint exp="" desc="" field="MinLevel"/>
    <constraint exp="" desc="" field="MaxLevel"/>
    <constraint exp="" desc="" field="Diameter"/>
    <constraint exp="" desc="" field="MinVolume"/>
    <constraint exp="" desc="" field="VolumeCurv"/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{abf0f75d-d540-4dba-95b7-0a5e773d384c}"/>
    <actionsetting action="" type="0" id="{8863574a-4d92-4ae1-b7f9-d021f1275b2a}" shortTitle="" capture="0" name="" icon="" notificationMessage="">
      <actionScope id="Field"/>
      <actionScope id="Canvas"/>
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" hidden="0" name="ID" width="-1"/>
      <column type="field" hidden="0" name="Elevation" width="-1"/>
      <column type="field" hidden="0" name="InitLevel" width="-1"/>
      <column type="field" hidden="0" name="MinLevel" width="-1"/>
      <column type="field" hidden="0" name="MaxLevel" width="-1"/>
      <column type="field" hidden="0" name="Diameter" width="-1"/>
      <column type="field" hidden="0" name="MinVolume" width="-1"/>
      <column type="field" hidden="0" name="VolumeCurv" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <editform>.</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="Diameter" editable="1"/>
    <field name="Elevation" editable="1"/>
    <field name="ID" editable="1"/>
    <field name="InitLevel" editable="1"/>
    <field name="MaxLevel" editable="1"/>
    <field name="MinLevel" editable="1"/>
    <field name="MinVolume" editable="1"/>
    <field name="VolumeCurv" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="Diameter"/>
    <field labelOnTop="0" name="Elevation"/>
    <field labelOnTop="0" name="ID"/>
    <field labelOnTop="0" name="InitLevel"/>
    <field labelOnTop="0" name="MaxLevel"/>
    <field labelOnTop="0" name="MinLevel"/>
    <field labelOnTop="0" name="MinVolume"/>
    <field labelOnTop="0" name="VolumeCurv"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>ID</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
