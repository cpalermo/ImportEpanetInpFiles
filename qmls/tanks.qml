<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" readOnly="0" version="3.0.0-Girona" simplifyDrawingTol="1" maxScale="0" minScale="0" simplifyAlgorithm="0" labelsEnabled="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" simplifyLocal="1">
  <renderer-v2 type="singleSymbol" forceraster="0" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" type="marker" alpha="1" clip_to_extent="1">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory scaleDependency="Area" barWidth="5" diagramOrientation="Up" backgroundColor="#ffffff" rotationOffset="0" penColor="#000000" penWidth="0" labelPlacementMethod="XHeight" scaleBasedVisibility="0" height="15" lineSizeScale="3x:0,0,0,0,0,0" minimumSize="0" maxScaleDenominator="1e+8" sizeType="MM" sizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" lineSizeType="MM" penAlpha="255" enabled="0" width="15" minScaleDenominator="0" opacity="1">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" obstacle="0" dist="0" priority="0" zIndex="0" linePlacementFlags="2" showAll="1">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties" type="Map">
          <Option name="positionX" type="Map">
            <Option value="true" name="active" type="bool"/>
            <Option value="ID" name="field" type="QString"/>
            <Option value="2" name="type" type="int"/>
          </Option>
          <Option name="positionY" type="Map">
            <Option value="true" name="active" type="bool"/>
            <Option value="ID" name="field" type="QString"/>
            <Option value="2" name="type" type="int"/>
          </Option>
          <Option name="show" type="Map">
            <Option value="true" name="active" type="bool"/>
            <Option value="ID" name="field" type="QString"/>
            <Option value="2" name="type" type="int"/>
          </Option>
        </Option>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="ID">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
    <alias field="ID" name="" index="0"/>
    <alias field="Elevation" name="" index="1"/>
    <alias field="InitLevel" name="" index="2"/>
    <alias field="MinLevel" name="" index="3"/>
    <alias field="MaxLevel" name="" index="4"/>
    <alias field="Diameter" name="" index="5"/>
    <alias field="MinVolume" name="" index="6"/>
    <alias field="VolumeCurv" name="" index="7"/>
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
    <constraint field="ID" notnull_strength="2" constraints="1" exp_strength="0" unique_strength="0"/>
    <constraint field="Elevation" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="InitLevel" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="MinLevel" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="MaxLevel" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="Diameter" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="MinVolume" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="VolumeCurv" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
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
    <defaultAction value="{65700e89-4f41-4ed8-a9d2-92ae998580d2}" key="Canvas"/>
    <actionsetting id="{abf0f75d-d540-4dba-95b7-0a5e773d384c}" action="" capture="0" name="" type="0" icon="" notificationMessage="" shortTitle="">
      <actionScope id="Field"/>
      <actionScope id="Feature"/>
      <actionScope id="Canvas"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="ID" type="field" width="-1" hidden="0"/>
      <column name="Elevation" type="field" width="-1" hidden="0"/>
      <column name="InitLevel" type="field" width="-1" hidden="0"/>
      <column name="MinLevel" type="field" width="-1" hidden="0"/>
      <column name="MaxLevel" type="field" width="-1" hidden="0"/>
      <column name="Diameter" type="field" width="-1" hidden="0"/>
      <column name="MinVolume" type="field" width="-1" hidden="0"/>
      <column name="VolumeCurv" type="field" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
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
    <field name="Diameter" labelOnTop="0"/>
    <field name="Elevation" labelOnTop="0"/>
    <field name="ID" labelOnTop="0"/>
    <field name="InitLevel" labelOnTop="0"/>
    <field name="MaxLevel" labelOnTop="0"/>
    <field name="MinLevel" labelOnTop="0"/>
    <field name="MinVolume" labelOnTop="0"/>
    <field name="VolumeCurv" labelOnTop="0"/>
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
