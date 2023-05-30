'use strict';

/*******************************************************************************************************************************************************************************************************
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*******************************************************************************************************************************************************************************************************/


/*******************************************************************************************************************************************************************************************************

*******************************************************************************************************************************************************************************************************/
// (function Kml (){
let altitude_decimals = false;

function isEmpty(obj) {
    // 判断对象是否为空（未定义、为null或为空字符串）
    return ( typeof obj === 'undefined' || obj === null  || obj === "") ;
}

// 定义枚举对象
let enums = {
    // 单位枚举
    unitsEnum: {
        fraction: "fraction", // 分数
        pixels: "pixels", // 像素
        insetPixels: "insetPixels" // 内缩像素
    },
    // 形状枚举
    shapeEnum: {
        rectangle: "rectangle", // 矩形
        cylinder: "cylinder", // 圆柱
        sphere: "sphere" // 球体
    },
    // 网格原点枚举
    gridOrigin: {
        lowerLeft: "lowerLeft", // 左下角
        upperLeft: "upperLeft" // 左上角
    },
    // 海拔模式枚举
    altitudeModeEnum: {
        clampToGround: "clampToGround", // 限制在地面
        clampToSeaFloor: "clampToSeaFloor", // 限制在海底
        relativeToGround: "relativeToGround", // 相对于地面
        relativeToSeaFloor: "relativeToSeaFloor", // 相对于海底
        absolute: "absolute" // 绝对
    },
    // 颜色模式枚举
    colorModeEnum: {
        normal: "normal", // 正常
        random: "random" // 随机
    },
    // 播放模式枚举
    playModeEnum: {
        pause: "pause" // 暂停
    },
    // 飞行模式枚举
    flyToModeEnum: {
        smooth: "smooth", // 平滑
        bounce: "bounce" // 弹跳
    },
    // 样式状态枚举
    styleStateEnum: {
        normal: "normal", // 正常
        highlight: "highlight" // 高亮
    },
    // 显示模式枚举
    displayModeEnum: {
        default: "default", // 默认
        hide: "hide" // 隐藏
    },
    // 项目图标模式枚举
    itemIconModeEnum: {
        open: "open", // 打开
        closed: "closed", // 关闭
        error: "error", // 错误
        fetching0: "fetching0", // 获取中0
        fetching1: "fetching1", // 获取中1
        fetching2: "fetching2" // 获取中2
    },
    // 刷新模式枚举
    refreshModeEnum: {
        onChange: "onChange", // 改变时
        onInterval: "onInterval", // 定时
        onExpire: "onExpire" // 到期
    },
    // 视图刷新模式枚举
    viewRefreshModeEnum: {
        never: "never", // 从不
        onStop: "onStop", // 停止时
        onRequest: "onRequest", // 请求时
        onRegion: "onRegion" // 区域变化时
    },
    // 列表项类型枚举
    listItemTypeEnum: {
        check: "check", // 复选框
        checkOffOnly: "checkOffOnly", // 仅取消选中
        checkHideChildren: "checkHideChildren", // 选中时隐藏子项
        radioFolder: "radioFolder" // 单选文件夹
    }
};

// Kml类定义
class Kml {
    // 构造函数
    constructor(feature, networkLinkControl) {
        this.features = []; // 特征数组初始化
        this.networkLinkControl = networkLinkControl; // 设置网络链接控制
        if (!isEmpty(feature)) // 如果feature非空
            this.features.push(feature); // 将feature添加到特征数组
    }
    // 将Kml对象转换为KML格式字符串
    toKml() {
        // KML的开始和结束标签
        const KML_START = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\">";
        const KML_END = "</kml>";

        // 将特征数组转换为KML格式字符串
        let featuresKml = (this.features.length > 0) ? this.features[0].toKml() : "";
        // 将网络链接控制转换为KML格式字符串
        let networkLinkControlKml = !isEmpty(this.networkLinkControl) ? this.networkLinkControl.toKml() : "";

        // 返回拼接后的KML字符串
        return KML_START + networkLinkControlKml + featuresKml + KML_END;
    }

    // 将给定的特征和网络链接控制包装为KML格式字符串
    static wrapKml(feature, networkLinkControl) {
        networkLinkControl = (typeof networkLinkControl !== 'undefined') ? networkLinkControl.toKml() : "";
        const KML_START = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\">";
        const KML_END = "</kml>";
        return KML_START + networkLinkControl + feature.toKml() + KML_END;
    }

    // 生成具有给定标签名和vec2对象的KML标签
    static tagVec2(tagName, vec2) {
        if (typeof vec2 === 'undefined')
            return "";
        if (typeof enums.unitsEnum[vec2.xunits] === 'undefined') {
            console.log(`Invalid xunits tag: ${tagName} units: ${vec2.xunits}`);
            return "";
        }
        if (typeof enums.unitsEnum[vec2.yunits] === 'undefined') {
            console.log(`Invalid xunits tag: ${tagName} units: ${vec2.yunits}`);
            return "";
        }
        return Kml.tag(tagName, 'empty', "", {
            x: vec2.x,
            y: vec2.y,
            xunits: vec2.xunits,
            yunits: vec2.yunits
        }, true);
    }
    // 定义一个静态方法，用于生成具有特定属性和内容的KML标签
    static tag(tagName, type, contents, attributes, notOptional) {
        // 定义一个检查角度范围的函数
        let checkAngle = function(min, max) {
            if (isNaN(contents)) {
                console.log(`Invalid ${type} value:${contents} tag:${tagName}`);
                return contents;
            }
            contents = +contents;
            if (contents < min || contents > max) {
                console.log(`Warning: angle exceeds expected range: ${type} value:${contents} tag:${tagName}`);
                contents = Kml.normalizeAngle(contents, min, max);
                console.log(`Normalized to: ${contents}`);
            }
            return;
        }
        // 检查内容是否为空或未定义
        if (typeof contents === 'undefined' || contents === null  || contents === "") {
            if (!notOptional && type !== 'empty')
                return "";
        }
        // 根据类型检查内容的有效性
        switch (type) {
        case 'boolean':
            if (contents === false || contents === 0)
                contents = "0";
            if (contents === true || contents === 1)
                contents = "1";
            if (contents !== "0" && contents !== "1") {
                console.log(`Invalid value:${contents} tag:${tagName}`)
                return ""
            }
            break;
        case 'string':
            if (typeof contents !== 'string') {
                console.log(`Warning: Possible invalid value:${contents} tag:${tagName}`)
                contents = String(contents);
            }
            if (/[&<]/g.test(contents)) {
                console.log(`Warning: Possible invalid characters value:${contents} tag:${tagName}`)
            }
            break;
        case 'html':
            contents = (!/[&<]/g.test(contents)) ? contents : Kml.wrapCDATA(contents);
            break;
        case 'xml':
            break;

        case 'altitudeMode':
            if (typeof enums.altitudeModeEnum[contents] === 'undefined') {
                console.log(`Invalid ${type} value:${contents} tag:${tagName}`);
                return "";
            }
            if (contents === enums.altitudeModeEnum.clampToSeaFloor || contents === enums.altitudeModeEnum.relativeToSeaFloor)
                tagName = "gx:altitudeMode";
            break;
        case 'color':
            let a = parseInt(contents, 16);
            if (typeof contents !== 'string' || contents.length !== 8 || a.toString(16).pad(8) !== contents.toLowerCase()) {
                console.log(`Invalid ${type} value:${contents} tag:${tagName}`);
                return "";
            }
            break;
        case 'angle90':
            checkAngle(-90, 90);
            break;
        case 'angle180':
            checkAngle(-180, 180);
            break;
        case 'angle360':
            checkAngle(-360, 360);
            break;
        case 'anglepos90':
            checkAngle(0, 90);
            break;
        case 'anglepos180':
            checkAngle(0, 180);
            break;
        case 'empty':
            if (!isEmpty(contents)) {
                console.log(`Warning: tag should have been empty: ${type} value:${contents} tag:${tagName}`);
            }
            break;
        case 'dateTime':
            //TODO: Validate
            break;
        case 'uri':
            //TODO: Validate
        case 'url':
            break;
        case 'coordinates':
            //TODO: Validate
            break;
        case 'int':
        case 'integer':
            if (isNaN(contents)) {
                console.log(`Invalid ${type} value:${contents} tag:${tagName}`);
                return "";
            }
            let num = (typeof contents === 'string') ? parseFloat(contents) : contents;
            if (num % 1 != 0)
                console.log(`Warning: integer expected, found float: ${type} value:${contents} tag:${tagName}`);
            break;
        case 'double':
        case 'float':
            if (isNaN(contents)) {
                console.log(`Invalid ${type} value:${contents} tag:${tagName}`);
                return "";
            }
            break;
        default:
            if (enums.hasOwnProperty(type)) {
                if (!enums[type].hasOwnProperty(contents)) {
                    console.log(`Invalid ${type} value:${contents} tag:${tagName}`);
                    return "";
                }
                break;
            }
            console.log(`Invalid type:${type} tag:${tagName}`)
            return "";
        }
        // 返回带有属性的KML标签
        return Kml.tagWithAttributes(tagName, contents, attributes);
    }

    // 定义一个静态方法，用于将角度规范化到指定的范围内
    static normalizeAngle(angle, min, max) {
        // 将字符串强制转换为数字，空字符串变为零
        angle = +angle;
        // 如果角度超出范围，将其调整到指定范围内
        if (angle < min || angle > max) {
            while (angle < min) {
                angle += (max - min);
            }
            while (angle > max) {
                angle -= (max - min);
            }
        }
        // 返回规范化后的角度值
        return angle;
    }

    // 定义一个静态方法，用于生成带有属性的KML标签
    static tagWithAttributes(tagName, contents, attributes) {
        let attributesKml = "";
        // 如果属性不为空，将其转换为KML格式的字符串
        if (!isEmpty(attributes)) {
            let attributeKeys = Object.keys(attributes);
            attributeKeys.forEach(key=>{
                let attribute=attributes[key];
                if (!isEmpty(attribute))
                    attributesKml+=" "+key+"=\""+attribute+"\"";
            });
        }
        // 如果内容不为空，将其添加到标签中，否则为空字符串
        contents = !isEmpty(contents) ? contents : "";
        // 返回带有属性和内容的KML标签
        return "<" + tagName + attributesKml + ">" + contents + "</" + tagName + ">";
    }

    static wrapCDATA(contents) {
        return "<![CDATA[" + contents + "]]>";
    }
}
/*******************************************************************************************************************************************************************************************************
<!-- abstract element; do not create -->
<!-- Object id="ID" targetId="NCName" -->
<!-- /Object> -->
******************************************************************************************************************************************************************************************************/
// 定义一个KML对象类
class KmlObject {
    // 构造函数可以接收ID和目标ID参数
    constructor(id, targetId) {
        this.id = id;
        this.targetId = targetId;
    }
    // 设置目标ID的方法，返回当前对象实例以便进行链式调用
    setTargetId(targetId) {
        this.targetId = targetId;
        return this;
    }
}
/*******************************************************************************************************************************************************************************************************
<!-- abstract element; do not create -->
<!-- Feature id="ID" -->                <!-- Document,Folder,
                                             NetworkLink,Placemark,
                                             GroundOverlay,PhotoOverlay,ScreenOverlay -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
  <atom:link href=" "/>            <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>    <!-- TimeStamp or TimeSpan -->
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>      <!-- new in KML 2.2 -->
<-- /Feature -->
******************************************************************************************************************************************************************************************************/
// 定义一个特征类，继承自KmlObject类
class Feature extends KmlObject {
    constructor(name, id, targetId) {
        super(id, targetId);
        this.name = name;
        this.styles = [];
    }

    // 设置描述信息的方法，返回当前对象实例以便进行链式调用
    setDescription(description) {
        this.description = description;
        return this;
    }

    // 设置可见性的方法，返回当前对象实例以便进行链式调用
    setVisibility(visibility) {
        this.visibility = visibility;
        return this;
    }

    // 设置打开状态的方法，返回当前对象实例以便进行链式调用
    setOpen(open) {
        this.open = open;
        return this;
    }

    // 设置抽象视图的方法，返回当前对象实例以便进行链式调用
    setAbstractView(abstractView) {
        this.abstractView = abstractView;
        return this;
    }

    // 设置时间戳的方法，返回当前对象实例以便进行链式调用
    setTimeStamp(when) {
        this.timePrimitive = new TimePrimitive('timeStamp',when);
        return this;
    }

    // 设置时间跨度的方法，返回当前对象实例以便进行链式调用
    setTimeSpan(begin, end) {
        this.timePrimitive = new TimePrimitive('timeSpan',begin,end);
        return this;
    }
    // 定义一个KML对象转换为KML字符串的方法
    toKml() {
        let kml = Kml.tag("name", 'string', this.name); // 将名称添加到KML字符串中
        kml += Kml.tag("visibility", 'boolean', this.visibility); // 将可见性添加到KML字符串中
        kml += Kml.tag("open", 'boolean', this.open); // 将打开状态添加到KML字符串中
        kml += Kml.tag("atom:author", 'xml', this.author, { // 将作者信息添加到KML字符串中
            "xmlns:atom": "http://www.w3.org/2005/Atom"
        });
        if (!isEmpty(this.linkHref)) // 如果链接地址不为空，将其添加到KML字符串中
            kml += Kml.tag("atom:link", 'string', null , {
                "xmlns:atom": "http://www.w3.org/2005/Atom",
                href: this.linkHref
            }, true);
        kml += Kml.tag("address", 'string', this.address); // 将地址信息添加到KML字符串中
        kml += Kml.tag("xal:AddressDetails", 'xml', this.addressDetails, { // 将详细地址信息添加到KML字符串中
            "xmlns:xal": "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
        });
        kml += Kml.tag("phoneNumber", 'string', this.phoneNumber); // 将电话号码添加到KML字符串中
        kml += Kml.tag("Snippet", 'string', this.snippet, { // 将摘要信息添加到KML字符串中
            maxLines: this.snippetMaxLines
        });
        kml += Kml.tag("description", 'html', this.description); // 将描述信息添加到KML字符串中
        if (!isEmpty(this.abstractView)) { // 如果抽象视图不为空，将其转换为KML字符串并添加到KML字符串中
            kml += this.abstractView.toKml();
        }
        if (!isEmpty(this.timePrimitive)) { // 如果时间基元不为空，将其转换为KML字符串并添加到KML字符串中
            kml += this.timePrimitive.toKml();
        }
        kml += Kml.tag("styleUrl", 'string', this.styleUrl); // 将样式链接添加到KML字符串中
        if (!isEmpty(this.styles)) { // 如果样式不为空，将其转换为KML字符串并添加到KML字符串中
            kml = this.styles.reduce((p, c)=>p+c.toKml(), kml);
        }
        if (!isEmpty(this.region)) { // 如果区域不为空，将其转换为KML字符串并添加到KML字符串中
            kml += this.region.toKml();
        }
        if (!isEmpty(this.extendedData)) { // 如果扩展数据不为空，将其转换为KML字符串并添加到KML字符串中
            kml += this.extendedData.toKml();
        }
        return kml; // 返回KML字符串
    }
}
/*******************************************************************************************************************************************************************************************************
<ExtendedData>
  <Data name="string">
    <displayName>...</displayName>    <!-- string -->
    <value>...</value>                <!-- string -->
  </Data>
  <SchemaData schemaUrl="anyURI">
    <SimpleData name=""> ... </SimpleData>   <!-- string -->
  </SchemaData>
  <namespace_prefix:other>...</namespace_prefix:other>
</ExtendedData>
******************************************************************************************************************************************************************************************************/
class ExtendedData {
    constructor() {
        this.datas = []; // 创建数据数组
    }
    addData(name, displayName, value) {
        let data = new Data(name,displayName,value); // 创建新的数据对象
        this.datas.push(data); // 将数据对象添加到数据数组中
        return this;
    }
    setSchemaDataUrl(schemaUrl) {
        if (isEmpty(this.schemaData)) // 如果模式数据为空，创建新的模式数据对象
            this.schemaData = new SchemaData(schemaUrl);
        else // 否则更新模式数据的模式链接
            this.schemaData.schemaUrl = schemaUrl;
        return this;
    }
    toKml() {
        let kml = this.datas.reduce((p, c)=>p+c.toKml(), ""); // 将数据数组中的数据对象转换为KML字符串并合并
        if (!isEmpty(this.schemaData)) { // 如果模式数据不为空，将其转换为KML字符串并添加到KML字符串中
            kml += this.schemaData.toKml();
        }
        //<namespace_prefix:other> tags not yet supported
        return Kml.tag("ExtendedData", 'xml', kml); // 返回ExtendedData元素的KML字符串表示形式
    }
}
/*******************************************************************************************************************************************************************************************************
  <Data name="string">
    <displayName>...</displayName>    <!-- string -->
    <value>...</value>                <!-- string -->
  </Data>
******************************************************************************************************************************************************************************************************/
class Data {
    constructor(name, displayName, value) {
        this.name = name; // 数据名称
        this.displayName = displayName; // 数据显示名称
        this.value = value; // 数据值
    }
    toKml() {
        let kml = Kml.tag("displayName", 'html', this.displayName); // 将displayName元素的KML字符串表示形式添加到kml字符串中
        kml += Kml.tag("value", 'string', this.value); // 将value元素的KML字符串表示形式添加到kml字符串中
        return Kml.tag("Data", 'xml', kml, { // 返回Data元素的KML字符串表示形式，包括数据名称属性
            name: this.name
        });
    }
}
/*******************************************************************************************************************************************************************************************************
  <SchemaData schemaUrl="anyURI">
    <SimpleData name=""> ... </SimpleData>   <!-- string -->
  </SchemaData>
******************************************************************************************************************************************************************************************************/
class SchemaData {
    constructor(schemaUrl) {
        this.schemaUrl = schemaUrl; // 模式URL
        this.simpleDatas = []; // SimpleData对象的数组
        this.simpleArrayDatas = []; // SimpleArrayData对象的数组
    }
    addSimpleData(name, contents) {
        let simpleData = new SimpleData(name,contents); // 创建新的SimpleData对象
        this.simpleDatas.push(simpleData); // 添加到simpleDatas数组中
        return this;
    }
    addSimpleArrayData(name, contents) {
        let simpleArrayData = new SimpleArrayData(name,contents); // 创建新的SimpleArrayData对象
        this.simpleArrayDatas.push(simpleArrayData); // 添加到simpleArrayDatas数组中
        return this;
    }
    toKml() {
        let kml = this.simpleDatas.reduce((p, c)=>p+c.toKml(), ""); // 将所有simpleDatas对象的KML字符串表示形式添加到kml字符串中
        kml = this.simpleArrayDatas.reduce((p, c)=>p+c.toKml(), kml); // 将所有simpleArrayDatas对象的KML字符串表示形式添加到kml字符串中
        return Kml.tag("SchemaData", 'xml', kml, { // 返回SchemaData元素的KML字符串表示形式，包括模式URL属性
            schemaUrl: this.schemaUrl
        });
    }
}

class SimpleData {
    constructor(name, contents) {
        this.name = name; // SimpleData名称
        this.contents = contents; // SimpleData内容
    }
    toKml() {
        return Kml.tag("SimpleData", 'string', this.contents, { // 返回SimpleData元素的KML字符串表示形式，包括名称属性和内容
            name: this.name
        });
    }
}

class SimpleArrayData {
    constructor(name, contents) {
        this.name = name; // SimpleArrayData名称
        if (typeof contents !== 'undefined') {
            this.contents = contents; // SimpleArrayData内容
        }
        else {
            this.contents = [];
        }
    }
    toKml() {
        let kml = this.contents.reduce((p, c)=>p+Kml.tag("gx:value", 'string', c), ""); // 将数组内容作为gx:value元素的子元素，将其转换为KML字符串
        return Kml.tag("gx:SimpleArrayData", 'xml', kml, {
            name: this.name // 返回SimpleArrayData元素的KML字符串表示形式，包括名称属性和子元素
        });
    }
}

/*******************************************************************************************************************************************************************************************************
<NetworkLink id="ID">
  <!-- inherited from Feature element --><name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
   <atom:link href=" "/>               <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>      <!-- new in KML 2.2 -->

  <!-- specific to NetworkLink -->
  <refreshVisibility>0</refreshVisibility> <!-- boolean -->
  <flyToView>0</flyToView>                 <!-- boolean -->
  <Link>...</Link>
</NetworkLink>
******************************************************************************************************************************************************************************************************/
class NetworkLink extends Feature {
    constructor(name, refreshVisibility, flyToView, link, id, targetId) {
        super(id, targetId);
        this.name = name;
        this.refreshVisibility = refreshVisibility;
        this.flyToView = flyToView;
        this.link = link;
    }
    toKml() {
        let kml = super.toKml();  // 调用父类 Feature 的 toKml 方法，获取 Feature 的 KML
        kml += Kml.tag("refreshVisibility", 'boolean', this.refreshVisibility);  // 添加 refreshVisibility 标签
        kml += Kml.tag("flyToView", 'boolean', this.flyToView);  // 添加 flyToView 标签
        if (!isEmpty(this.link))  // 如果 Link 对象存在
            kml += this.link.toKml();  // 添加 Link 对象的 KML
        return Kml.tag("NetworkLink", 'xml', kml, {  // 创建 NetworkLink 标签
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<NetworkLinkControl>
  <minRefreshPeriod>0</minRefreshPeriod>           <!-- float -->
  <maxSessionLength>-1</maxSessionLength>          <!-- float -->
  <cookie>...</cookie>                             <!-- string -->
  <message>...</message>                           <!-- string -->
  <linkName>...</linkName>                         <!-- string -->
  <linkDescription>...</linkDescription>           <!-- string -->
  <linkSnippet maxLines="2">...</linkSnippet>      <!-- string -->
  <expires>...</expires>                           <!-- kml:dateTime -->
  <Update>...</Update>                             <!-- Change,Create,Delete -->
  <AbstractView>...</AbstractView>                 <!-- LookAt or Camera -->
</NetworkLinkControl>
******************************************************************************************************************************************************************************************************/
class NetworkLinkControl {
    constructor() {
        this.update = new Update();
    }
    addChange(change) {
        if (isEmpty(this.update.change))
            this.update.change = new Change();
        this.update.change.changes.push(change);
        return this;
    }
    addCreate(create) {
        if (isEmpty(this.update.create))
            this.update.create = new Create();
        this.update.create.creates.push(create);
        return this;
    }
    addDelete(_delete) {
        if (isEmpty(this.update.delete))
            this.update.delete = new Delete();
        this.update.delete.deletes.push(_delete);
        return this;
    }
    toKml() {
        let kml = Kml.tag("minRefreshPeriod", 'float', this.minRefreshPeriod);
        kml += Kml.tag("maxSessionLength", 'float', this.maxSessionLength);
        kml += Kml.tag("cookie", 'string', this.cookie);
        kml += Kml.tag("message", 'string', this.message);
        kml += Kml.tag("linkName", 'string', this.linkName);
        kml += Kml.tag("linkDescription", 'string', this.linkDescription);
        kml += Kml.tag("linkSnippet", 'string', this.linkSnippet, {
            maxLines: this.linkSnippetMaxLines
        });
        kml += Kml.tag("expires", 'dateTime', this.expires);
        if (!isEmpty(this.update))
            kml += this.update.toKml();
        if (!isEmpty(this.abstractView))
            kml += this.abstractView.toKml();
        return Kml.tag("NetworkLinkControl", 'xml', kml);
    }
}
/*******************************************************************************************************************************************************************************************************
<Link id="ID">
  <!-- specific to Link -->
  <href>...</href>                      <!-- string -->
  <refreshMode>onChange</refreshMode>
    <!-- refreshModeEnum: onChange, onInterval, or onExpire -->
  <refreshInterval>4</refreshInterval>  <!-- float -->
  <viewRefreshMode>never</viewRefreshMode>
    <!-- viewRefreshModeEnum: never, onStop, onRequest, onRegion -->
  <viewRefreshTime>4</viewRefreshTime>  <!-- float -->
  <viewBoundScale>1</viewBoundScale>    <!-- float -->
  <viewFormat>BBOX=[bboxWest],[bboxSouth],[bboxEast],[bboxNorth]</viewFormat>
                                        <!-- string -->
  <httpQuery>...</httpQuery>            <!-- string -->
</Link>
******************************************************************************************************************************************************************************************************/
class Link extends KmlObject {
    constructor(href, id, targetId) {
        super(id, targetId);
        this.href = href;
    }
    setRefresh(refreshMode, refreshInterval) {
        this.refreshMode = refreshMode;
        this.refreshInterval = refreshInterval;
        return this;
    }
    setViewRefresh(viewRefreshMode, viewRefreshTime) {
        this.viewRefreshMode = viewRefreshMode;
        this.viewRefreshTime = viewRefreshTime;
        return this;
    }
    toKml() {
        let kml = Kml.tag("href", 'string', this.href);
        kml += Kml.tag("refreshMode", 'refreshModeEnum', this.refreshMode);
        kml += Kml.tag("refreshInterval", 'float', this.refreshInterval);
        kml += Kml.tag("viewRefreshMode", 'viewRefreshModeEnum', this.viewRefreshMode);
        kml += Kml.tag("viewRefreshTime", 'float', this.viewRefreshTime);
        kml += Kml.tag("viewBoundScale", 'float', this.viewBoundScale);
        kml += Kml.tag("viewFormat", 'xml', this.viewFormat);
        kml += Kml.tag("httpQuery", 'string', this.httpQuery);
        return Kml.tag("Link", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
    static getViewFormatStringAll() {
        return "BBOX=[bboxWest],[bboxSouth],[bboxEast],[bboxNorth]&amp;LookAt=[lookatLon],[lookatLat],[lookatRange],[lookatTilt],[lookatHeading],[lookatTerrainLon],[lookatTerrainLat],[lookatTerrainAlt]&amp;Camera=[cameraLon],[cameraLat],[cameraAlt],[horizFov],[vertFov]&amp;Other=[horizPixels],[vertPixels],[terrainEnabled]";
    }
}

/*******************************************************************************************************************************************************************************************************
<!-- abstract element; do not create -->
<!-- Container id="ID" -->              <!-- Document,Folder -->
  <!-- inherited from Feature element -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <address>...</address>                <!-- string -->
  <AddressDetails xmlns="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0">...
      </AddressDetails>                 <!-- string -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- LookAt or Camera -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>
  <atom:author>...<atom:author>   <!-- xmlns:atom="http://www.w3.org/2005/Atom" -->
  <atom:link href=" "/>

  <!-- specific to Container -->
  <!-- 0 or more Features -->
<!-- /Container -->
******************************************************************************************************************************************************************************************************/
class Container extends Feature {
    constructor(name, id, targetId) {
        super(name, id, targetId);
    }
    toKml() {
        let kml = super.toKml();
        return kml;
    }
}
/*******************************************************************************************************************************************************************************************************
<Folder id="ID">
  <!-- inherited from Feature element -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
  <atom:link href=" "/>            <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>

  <!-- specific to Folder -->
  <!-- 0 or more Feature elements -->
</Folder>
******************************************************************************************************************************************************************************************************/
class Folder extends Container {
    constructor(name, id, targetId) {
        super(name, id, targetId);
        this.features = [];
    }
    toKml() {
        let kml = super.toKml();
        kml = this.features.reduce((p, c)=>p+c.toKml(), kml);
        return Kml.tag("Folder", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Document id="ID">
  <!-- inherited from Feature element -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
  <atom:link href=" "/>                 <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>      <!-- new in KML 2.2 -->

  <!-- specific to Document -->
  <!-- 0 or more Schema elements -->
  <!-- 0 or more Feature elements -->
</Document>
******************************************************************************************************************************************************************************************************/
class Document extends Container {
    constructor(name, id, targetId) {
        super(name, id, targetId);
        this.schemas = [];
        this.features = [];
    }
    toKml() {
        let kml = super.toKml();
        kml = this.schemas.reduce((p, c)=>p+c.toKml(), kml);
        kml = this.features.reduce((p, c)=>p+c.toKml(), kml);
        return Kml.tag("Document", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Schema name="string" id="ID">
  <SimpleField type="string" name="string">
    <displayName>...</displayName>            <!-- string -->
  </SimpleField>
</Schema>
******************************************************************************************************************************************************************************************************/
class Schema {
    constructor(name, id) {
        this.name = name;
        this.id = id;
        this.simpleFields = [];
    }
    addSimpleField(type, name, displayName) {
        this.simpleFields.push(new SimpleField(type,name,displayName));
        return this;
    }
    addSimpleArrayField(type, name, displayName) {
        this.simpleFields.push(new SimpleField(type,name,displayName));
        return this;
    }
    toKml() {
        let kml = this.simpleFields.reduce((p, c)=>p+c.toKml(), "");
        return Kml.tag("Schema ", 'xml', kml, {
            name: this.name,
            id: this.id
        }, true);
    }
}
class SimpleField {
    constructor(type, name, displayName) {
        this.type = type;
        this.name = name;
        this.displayName = displayName;
    }
    toKml() {
        let kml = Kml.tag("displayName", 'html', this.displayName);
        return Kml.tag("SimpleField", 'xml', kml, {
            type: this.type,
            name: this.name
        }, true);
    }
}
class SimpleArrayField {
    constructor(type, name, displayName) {
        this.type = type;
        this.name = name;
        this.displayName = displayName;
    }
    toKml() {
        let kml = Kml.tag("displayName", 'html', this.displayName);
        return Kml.tag("gx:SimpleArrayField", 'xml', kml, {
            type: this.type,
            name: this.name
        }, true);
    }
}

/*******************************************************************************************************************************************************************************************************
<!-- abstract element; do not create -->
<!-- Geometry id="ID" -->
                                              <!-- Point,LineString,LinearRing,
                                               Polygon,MultiGeometry,Model,
                                               gx:Track -->
<!-- /Geometry -->
******************************************************************************************************************************************************************************************************/
class Geometry extends KmlObject {
    constructor(type, coordinates, id, targetId) {
        super(id, targetId);
        this.type = type;
        if (!isEmpty(coordinates)) {
            this.setCoordinates(coordinates);
        }
    }
    setCoordinates(coordinates) {
        // if single coordinate is passed in convert to array
        coordinates = !isEmpty(coordinates) ? (Array.isArray(coordinates) ? coordinates : [coordinates]) : [];
        if (this.type === 'Polygon') {
            this.outerBoundaryIs = new OuterBoundaryIs(new LinearRing(coordinates));
        } else {
            this.coordinates = coordinates;
        }
        return this;
    }
    removeDuplicates(isRing) {
        let i = 1;
        while (i < this.coordinates.length) {
            if (this.coordinates[i].equals(this.coordinates[i - 1]))
                this.coordinates.splice(i, 1);
            else
                i += 1;
        }
        if (isRing && this.coordinates.length > 1 && this.coordinates[0].equals(this.coordinates[this.coordinates.length - 1]))
            this.coordinates.pop();
    }
    coordinatesToKml(isRing) {
        let kml = " ";
        if (typeof this.coordinates !== 'undefined') {
            this.removeDuplicates();
            for (let i = 0; i < this.coordinates.length; i += 1) {
                kml += this.coordinates[i].toKml();
            }
            // first point is duplicated at end in Polygons
            if (isRing && this.coordinates.length > 0) {
                kml += this.coordinates[0].toKml();
            }
        }
        return kml;
    }
    static area(coordinates) {
        return Math.abs(this.areaAndPerimeter(coordinates).area.toFixed(1));
    }
    static perimeter(coordinates) {
        return this.areaAndPerimeter(coordinates).perimeter.toFixed(3);
    }
    static areaAndPerimeter(coordinates) {
        let geod = GeographicLib.Geodesic.WGS84;
        let polygon = geod.Polygon(false);
        coordinates.forEach(coordinate=>polygon.AddPoint(coordinate.lat, coordinate.lng));
        return polygon.Compute(true, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<LineString id="ID">
  <!-- specific to LineString -->
  <gx:altitudeOffset>0</gx:altitudeOffset>  <!-- double -->
  <extrude>0</extrude>                      <!-- boolean -->
  <tessellate>0</tessellate>                <!-- boolean -->
  <altitudeMode>clampToGround</altitudeMode>
      <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
      <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
  <gx:drawOrder>0</gx:drawOrder>            <!-- integer -->
  <coordinates>...</coordinates>            <!-- lon,lat[,alt] -->
</LineString>
******************************************************************************************************************************************************************************************************/
class LineString extends Geometry {
    constructor(coordinates, tessellate, id, targetId) {
        super("LineString", coordinates, id, targetId);
        this.tessellate = tessellate;
    }
    toKml() {
        let kml = Kml.tag("gx:altitudeOffset", 'double', this.altitudeOffset);
        kml += Kml.tag("extrude", 'boolean', this.extrude);
        kml += Kml.tag("tessellate", 'boolean', this.tessellate);
        kml += Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        kml += Kml.tag("gx:drawOrder", 'integer', this.drawOrder);
        kml += Kml.tag("coordinates", 'coordinates', this.coordinatesToKml());
        return Kml.tag("LineString", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Point id="ID">
  <!-- specific to Point -->
  <extrude>0</extrude>                        <!-- boolean -->
  <altitudeMode>clampToGround</altitudeMode>
        <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
        <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
  <coordinates>...</coordinates>              <!-- lon,lat[,alt] -->
</Point>
******************************************************************************************************************************************************************************************************/
class Point extends Geometry {
    constructor(coordinates, id, targetId) {
        super('Point', coordinates, id, targetId);
    }
    toKml() {
        let kml = Kml.tag("extrude", 'boolean', this.extrude);
        kml += Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        kml += Kml.tag("gx:drawOrder", 'integer', this.drawOrder);
        kml += Kml.tag("coordinates", 'coordinates', this.coordinatesToKml());
        return Kml.tag("Point", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<MultiGeometry id="ID">
  <!-- specific to MultiGeometry -->
  <!-- 0 or more Geometry elements -->
</MultiGeometry>
******************************************************************************************************************************************************************************************************/
class MultiGeometry extends Geometry {
    constructor(id, targetId) {
        super('MultiGeometry', undefined, id, targetId);
        this.geometries = [];
    }
    toKml() {
        let kml = this.geometries.reduce((p, c)=>p+c.toKml(), "");
        return Kml.tag("MultiGeometry", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Polygon id="ID">
  <!-- specific to Polygon -->
  <extrude>0</extrude>                       <!-- boolean -->
  <tessellate>0</tessellate>                 <!-- boolean -->
  <altitudeMode>clampToGround</altitudeMode>
        <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
        <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
  <outerBoundaryIs>
    <LinearRing>
      <coordinates>...</coordinates>         <!-- lon,lat[,alt] -->
    </LinearRing>
  </outerBoundaryIs>
  <innerBoundaryIs>
    <LinearRing>
      <coordinates>...</coordinates>         <!-- lon,lat[,alt] -->
    </LinearRing>
  </innerBoundaryIs>
</Polygon>
******************************************************************************************************************************************************************************************************/
class Polygon extends Geometry {
    constructor(coordinates, tessellate, id, targetId) {
        super('Polygon', coordinates, id, targetId);
        this.tessellate = tessellate;
        this.innerBoundaryIss = [];
    }
    addInnerBoundary(coordinates) {
        this.innerBoundaryIss.push(new InnerBoundaryIs(new LinearRing(coordinates)));
        return this;
    }
    toKml() {
        let kml = Kml.tag("extrude", 'boolean', this.extrude);
        kml += Kml.tag("tessellate", 'boolean', this.tessellate);
        kml += Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        if (!isEmpty(this.outerBoundaryIs)) {
            kml += this.outerBoundaryIs.toKml();
        }
        kml = this.innerBoundaryIss.reduce((p, c)=>p+c.toKml(), kml);
        return Kml.tag("Polygon", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
  <outerBoundaryIs>
    <LinearRing>
      <coordinates>...</coordinates>         <!-- lon,lat[,alt] -->
    </LinearRing>
  </outerBoundaryIs>
  <innerBoundaryIs>
    <LinearRing>
      <coordinates>...</coordinates>         <!-- lon,lat[,alt] -->
    </LinearRing>
  </innerBoundaryIs>
******************************************************************************************************************************************************************************************************/
class OuterBoundaryIs {
    constructor(linearRing) {
        this.linearRing = linearRing;
    }
    toKml() {
        if (!isEmpty(this.linearRing)) {
            return Kml.tag("outerBoundaryIs", 'xml', this.linearRing.toKml());
        }
    }
}
class InnerBoundaryIs {
    constructor(linearRing) {
        //Google Earth appears to convert multimple innerBoundaryIs to a single one with multiple linearRings
        this.linearRings = [];
        if (typeof linearRing !== 'undefined')
            this.linearRings.push(linearRing);
    }
    toKml() {
        let kml = this.linearRings.reduce((p, c)=>p+c.toKml(), "");
        return Kml.tag("innerBoundaryIs", 'xml', kml);
    }
}
/*******************************************************************************************************************************************************************************************************
<LinearRing id="ID">
  <!-- specific to LinearRing -->
  <gx:altitudeOffset>0</gx:altitudeOffset>   <!-- double -->
  <extrude>0</extrude>                       <!-- boolean -->
  <tessellate>0</tessellate>                 <!-- boolean -->
  <altitudeMode>clampToGround</altitudeMode>
    <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
    <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
  <coordinates>...</coordinates>             <!-- lon,lat[,alt] tuples -->
</LinearRing>
******************************************************************************************************************************************************************************************************/
class LinearRing extends Geometry {
    constructor(coordinates, tessellate, id, targetId) {
        super('LinearRing', coordinates, id, targetId);
        this.tessellate = tessellate;
    }
    toKml() {
        let kml = Kml.tag("gx:altitudeOffset", 'double', this.altitudeOffset);
        Kml.tag("extrude", 'boolean', this.extrude);
        kml += Kml.tag("tessellate", 'boolean', this.tessellate);
        kml += Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        kml += Kml.tag("coordinates", 'coordinates', this.coordinatesToKml(true));
        return Kml.tag("LinearRing", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Model id="ID">
<!-- specific to Model -->
<altitudeMode>clampToGround</altitudeMode>
    <!-- kml:altitudeModeEnum: clampToGround,relativeToGround,or absolute -->
    <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
<Location>
  <longitude></longitude> <!-- kml:angle180 -->
  <latitude></latitude>   <!-- kml:angle90 -->
  <altitude>0</altitude>  <!-- double -->
</Location>
<Orientation>
  <heading>0</heading>    <!-- kml:angle360 -->
  <tilt>0</tilt>          <!-- kml:anglepos180 -->
  <roll>0</roll>          <!-- kml:angle180 -->
</Orientation>
<Scale>
  <x>1</x>                <!-- double -->
  <y>1</y>                <!-- double -->
  <z>1</z>                <!-- double -->
</Scale>
<Link>...</Link>
<ResourceMap>
  <Alias>
    <targetHref>...</targetHref>   <!-- anyURI -->
    <sourceHref>...</sourceHref>   <!-- anyURI -->
  </Alias>
</ResourceMap>
</Model>
******************************************************************************************************************************************************************************************************/
class Model extends Geometry {
    constructor(altitudeMode, location, orientation, scale, link, resourceMap, id, targetId) {
        super(null , id, targetId);
        this.altitudeMode = altitudeMode;
        this.location = location;
        this.orientation = orientation;
        this.scale = scale;
        this.link = link;
        this.resourceMap = resourceMap;
    }
    toKml() {
        let kml = Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        if (typeof this.location !== 'undefined')
            kml += this.location.toKml();
        if (typeof this.orientation !== 'undefined')
            kml += this.orientation.toKml();
        if (typeof this.scale !== 'undefined')
            kml += this.scale.toKml();
        if (typeof this.link !== 'undefined')
            kml += this.link.toKml();
        if (typeof this.resourceMap !== 'undefined')
            kml += this.resourceMap.toKml();
        return Kml.tag("Model", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Location>
	<longitude>39.55375305703105</longitude>
	<latitude>-118.9813220168456</latitude>
	<altitude>1223</altitude>
</Location>
******************************************************************************************************************************************************************************************************/
class Location extends KmlObject {
    constructor(longitude, latitude, altitude, id, targetId) {
        super(id, targetId);
        this.longitude = longitude;
        this.latitude = latitude;
        this.altitude = altitude;
    }
    toKml() {
        let kml = Kml.tag("longitude", 'angle180', this.longitude);
        kml += Kml.tag("latitude", 'angle90', this.latitude);
        kml += Kml.tag("altitude", 'double', this.altitude);
        return Kml.tag("Location", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Orientation>
  <heading>45.0</heading>
  <tilt>10.0</tilt>
  <roll>0.0</roll>
</Orientation>
******************************************************************************************************************************************************************************************************/
class Orientation extends KmlObject {
    constructor(heading, tilt, roll, id, targetId) {
        super(id, targetId);
        this.heading = heading;
        this.tilt = tilt;
        this.roll = roll;
    }
    toKml() {
        let kml = Kml.tag("heading", 'angle360', this.heading);
        kml += Kml.tag("tilt", 'anglepos180', this.tilt);
        kml += Kml.tag("roll", 'angle180', this.roll);
        return Kml.tag("Orientation", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Scale>
	<x>1</x>                <!-- double -->
	<y>1</y>                <!-- double -->
	<z>1</z>                <!-- double -->
</Scale>
******************************************************************************************************************************************************************************************************/
class Scale extends KmlObject {
    constructor(x, y, z, id, targetId) {
        super(id, targetId);
        this.x = x;
        this.y = y;
        this.z = z;
    }
    toKml() {
        let kml = Kml.tag("x", 'double', this.x);
        kml += Kml.tag("y", 'double', this.y);
        kml += Kml.tag("z", 'double', this.z);
        return Kml.tag("Scale", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<ResourceMap>
  <Alias>
    <targetHref>../images/foo.jpg</targetHref>
    <sourceHref>c:\mytextures\foo.jpg</sourceHref>
  </Alias>
</ResourceMap>
******************************************************************************************************************************************************************************************************/
class ResourceMap extends KmlObject {
    constructor(id, targetId) {
        super(id, targetId);
        this.aliass = [];
    }
    addAlias(targetHref, sourceHref) {
        let alias = new Alias(targetHref,sourceHref);
        this.aliass.push(alias);
        return this;
    }
    toKml() {
        let kml = this.aliass.reduce((p, c)=>p+c.toKml(), "");
        return Kml.tag("ResourceMap", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
class Alias {
    constructor(targetHref, sourceHref) {
        this.targetHref = targetHref;
        this.sourceHref = sourceHref;
    }
    toKml() {
        let kml = Kml.tag("targetHref", 'string', this.targetHref);
        kml += Kml.tag("sourceHref", 'string', this.sourceHref);
        return Kml.tag("Alias", 'xml', kml)
    }
}
/*******************************************************************************************************************************************************************************************************
<Placemark id="ID">
  <!-- inherited from Feature element -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
  <atom:link href=" "/>                <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>      <!-- new in KML 2.2 -->

  <!-- specific to Placemark element -->
  <Geometry>...</Geometry>
</Placemark>
******************************************************************************************************************************************************************************************************/
class Placemark extends Feature {
    constructor(type, name, styleUrl, coordinates, id, targetId) {
        super(name, id, targetId);
        this.type = type;
        this.styleUrl = styleUrl;
        if (!isEmpty(type)) {
            switch (type) {
            case "LineString":
                this.geometry = new LineString(coordinates,"1");
                break;
            case "Point":
                this.geometry = new Point(coordinates);
                break;
            case "Polygon":
                this.geometry = new Polygon(coordinates,"1");
                break;
            case "MultiGeometry":
                this.geometry = new MultiGeometry();
                break;
            case "LinearRing":
                this.geometry = new LinearRing(coordinates,"1");
                break;
            case "Model":
                //construct seperately
                break;
            default:
            case "Track":
                //construct seperately
                break;
                console.log("Warning: unknown placemark type");
            }
        }
    }
    setModel(altitudeMode, location, orientation, scale, link, resourceMap, id, targetId) {
        this.geometry = new Model(altitudeMode,location,orientation,scale,link,resourceMap,id,targetId);
        return this;
    }
    setAltitudeMode(altitudeMode) {
        this.geometry.altitudeMode = altitudeMode;
        return this;
    }

    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("gx:balloonVisibility", 'boolean', this.balloonVisibility);
        if (typeof this.geometry != 'undefined')
            kml += this.geometry.toKml();
        return Kml.tag("Placemark", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<!-- abstract element; do not create -->
<!-- StyleSelector id="ID" -->                 <!-- Style,StyleMap -->
<!-- /StyleSelector -->
******************************************************************************************************************************************************************************************************/
class StyleSelector extends KmlObject {
    constructor(id, targetId) {
        super(id, targetId);
    }
}
/*******************************************************************************************************************************************************************************************************
<StyleMap id="ID">
  <!-- extends StyleSelector -->
  <!-- elements specific to StyleMap -->
  <Pair id="ID">
    <key>normal</key>              <!-- kml:styleStateEnum:  normal or highlight -->
    <styleUrl>...</styleUrl> or <Style>...</Style>
  </Pair>
</StyleMap>
******************************************************************************************************************************************************************************************************/
class StyleMap extends StyleSelector {
    constructor(normal, highlight, id, targetId) {
        super(id, targetId);
        this.pairs = [];
        if (!isEmpty(normal)) {
            let normalPair = new Pair("normal");
            if (typeof normal === 'string')
                normalPair.styleUrl = normal;
            if (normal instanceof Style)
                normalPair.style = normal;
            this.pairs.push(normalPair);
        }
        if (!isEmpty(highlight)) {
            let highlightPair = new Pair("highlight");
            if (typeof highlight === 'string')
                highlightPair.styleUrl = highlight;
            if (highlight instanceof Style)
                highlightPair.style = highlight;
            this.pairs.push(highlightPair);
        }
    }
    toKml() {
        let kml = this.pairs.reduce((p, c)=>p+c.toKml(), "");
        return Kml.tag("StyleMap", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
 <Pair id="ID">
    <key>normal</key>              <!-- kml:styleStateEnum:  normal or highlight -->
    <styleUrl>...</styleUrl> or <Style>...</Style>
  </Pair>
******************************************************************************************************************************************************************************************************/
class Pair extends StyleSelector {
    constructor(key, id, targetId) {
        super(id, targetId);
        this.key = key;
    }
    toKml() {
        let kml = Kml.tag("key", 'styleStateEnum', this.key);
        if (!isEmpty(this.styleUrl))
            kml += Kml.tag("styleUrl", 'string', this.styleUrl);
        if (!isEmpty(this.style))
            kml += this.style.toKml();
        return Kml.tag("Pair", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<Style id="ID">
<!-- extends StyleSelector -->

<!-- specific to Style -->
  <IconStyle>...</IconStyle>
  <LabelStyle>...</LabelStyle>
  <LineStyle>...</LineStyle>
  <PolyStyle>...</PolyStyle>
  <BalloonStyle>...</BalloonStyle>
  <ListStyle>...</ListStyle>
</Style>
******************************************************************************************************************************************************************************************************/
class Style extends StyleSelector {
    constructor(id, targetId) {
        super(id, targetId);
    }
    setLineStyle(color, width) {
        this.lineStyle = new LineStyle(color,width);
        return this;
    }
    setPolyStyle(color, fill, outline) {
        this.polyStyle = new PolyStyle(color,fill,outline);
        return this;
    }
    setNoFill() {
        this.setPolyStyle("", "0");
        return this;
    }
    setIconStyle(color, scale, iconHref, heading) {
        this.iconStyle = new IconStyle(color,scale,iconHref,heading);
        return this;
    }
    setNoIcon() {
        this.iconStyle = new IconStyle();
        return this;
    }
    setRadioListStyle() {
        this.listStyle = new ListStyle()
        this.listStyle.listItemType = "radioFolder";
        return this;
    }
    setLabelStyle(color, scale) {
        this.labelStyle = new LabelStyle(color,scale);
        return this;
    }
    setIconHotSpot(x, y, xunits, yunits) {
        if (typeof this.iconStyle === 'undefined')
            this.iconStyle = new IconStyle();
        this.iconStyle.setHotSpot(x, y, xunits, yunits);
        return this;
    }
    setBalloonStyle(bgColor, textColor, text, displayMode) {
        this.balloonStyle = new BalloonStyle(bgColor,textColor,text,displayMode);
        return this;
    }
    toKml() {
        let kml = "";
        if (!isEmpty(this.lineStyle))
            kml += this.lineStyle.toKml();
        if (!isEmpty(this.polyStyle))
            kml += this.polyStyle.toKml();
        if (!isEmpty(this.iconStyle))
            kml += this.iconStyle.toKml();
        if (!isEmpty(this.labelStyle))
            kml += this.labelStyle.toKml();
        if (!isEmpty(this.balloonStyle))
            kml += this.balloonStyle.toKml();
        if (!isEmpty(this.listStyle))
            kml += this.listStyle.toKml();
        return Kml.tag("Style", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/********************************************************************
********************************************************************/
class SubStyle extends KmlObject {

}
/*******************************************************************************************************************************************************************************************************
<BalloonStyle id="ID">
  <!-- specific to BalloonStyle -->
  <bgColor>ffffffff</bgColor>            <!-- kml:color -->
  <textColor>ff000000</textColor>        <!-- kml:color -->
  <text>...</text>                       <!-- string -->
  <displayMode>default</displayMode>     <!-- kml:displayModeEnum -->
</BalloonStyle>
******************************************************************************************************************************************************************************************************/
class BalloonStyle extends SubStyle {
    constructor(bgColor, textColor, text, displayMode, id, targetId) {
        super(id, targetId);
        this.bgColor = bgColor;
        this.textColor = textColor;
        this.text = text;
        this.displayMode = displayMode;
    }
    toKml() {
        let kml = Kml.tag("bgColor", 'color', this.bgColor);
        kml += Kml.tag("textColor", 'color', this.textColor);
        kml += Kml.tag("text", 'html', this.text);
        kml += Kml.tag("displayMode", 'displayModeEnum', this.displayMode);
        return Kml.tag("BalloonStyle", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<ListStyle id="ID">
  <!-- specific to ListStyle -->
  <listItemType>check</listItemType> <!-- kml:listItemTypeEnum:check,
                                          checkOffOnly,checkHideChildren,
                                         radioFolder -->
  <bgColor>ffffffff</bgColor>        <!-- kml:color -->
  <ItemIcon>                         <!-- 0 or more ItemIcon elements -->
    <state>open</state>
      <!-- kml:itemIconModeEnum:open, closed, error, fetching0, fetching1, or fetching2 -->
    <href>...</href>                 <!-- anyURI -->
  </ItemIcon>
</ListStyle>
******************************************************************************************************************************************************************************************************/
class ListStyle extends SubStyle {
    constructor(id, targetId) {
        super(id, targetId);
        this.itemIcons = [];
    }
    addItemIcon(state, href) {
        let itemIcon = new ItemIcon(state,href);
        this.itemIcons.push(itemIcon);
    }
    toKml() {
        let kml = Kml.tag("listItemType", 'listItemTypeEnum', this.listItemType);
        kml += Kml.tag("bgColor", 'color', this.bgColor);
        kml = this.itemIcons.reduce((p, c)=>p+c.toKml(), kml);
        return Kml.tag("ListStyle", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
class ItemIcon {
    constructor(state, href) {
        this.state = state;
        this.href = href;
    }
    toKml() {
        let kml = Kml.tag("state", 'itemIconModeEnum', this.state);
        kml += Kml.tag("href", 'uri', this.href);
        return Kml.tag("ItemIcon", 'xml', kml);
    }
}

/*******************************************************************************************************************************************************************************************************
<!-- abstract element; do not create -->
<!-- ColorStyle id="ID" -->          <!-- IconStyle,LabelStyle,LineStyle,PolyStyle -->
  <color>ffffffff</color>            <!-- kml:color -->
  <colorMode>normal</colorMode>      <!-- kml:colorModeEnum: normal or random -->
<!-- /ColorStyle -->
******************************************************************************************************************************************************************************************************/
class ColorStyle extends SubStyle {
    constructor(id, targetId) {
        super(id, targetId);
    }
    toKml() {
        let kml = Kml.tag("color", 'color', this.color);
        kml += Kml.tag("colorMode", 'colorModeEnum', this.colorMode);
        return kml;
    }
}
/*******************************************************************************************************************************************************************************************************
<LineStyle id="ID">
  <!-- inherited from ColorStyle -->
  <color>ffffffff</color>            <!-- kml:color -->
  <colorMode>normal</colorMode>      <!-- colorModeEnum: normal or random -->

  <!-- specific to LineStyle -->
  <width>1</width>                            <!-- float -->
  <gx:outerColor>ffffffff</gx:outerColor>     <!-- kml:color -->
  <gx:outerWidth>0.0</gx:outerWidth>          <!-- float -->
  <gx:physicalWidth>0.0</gx:physicalWidth>    <!-- float -->
  <gx:labelVisibility>0</gx:labelVisibility>  <!-- boolean -->
</LineStyle>
******************************************************************************************************************************************************************************************************/
class LineStyle extends ColorStyle {
    constructor(color, width, id, targetId) {
        super(id, targetId);
        this.color = color;
        this.width = width;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("width", 'float', this.width);
        kml += Kml.tag("gx:outerColor", 'color', this.outerColor);
        kml += Kml.tag("gx:outerWidth", 'float', this.outerWidth);
        kml += Kml.tag("gx:physicalWidth", 'float', this.physicalWidth);
        kml += Kml.tag("gx:labelVisibility", 'boolean', this.labelVisibility);
        return Kml.tag("LineStyle", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<PolyStyle id="ID">
  <!-- inherited from ColorStyle -->
  <color>ffffffff</color>            <!-- kml:color -->
  <colorMode>normal</colorMode>      <!-- kml:colorModeEnum: normal or random -->

  <!-- specific to PolyStyle -->
  <fill>1</fill>                     <!-- boolean -->
  <outline>1</outline>               <!-- boolean -->
</PolyStyle>
******************************************************************************************************************************************************************************************************/
class PolyStyle extends ColorStyle {
    constructor(color, fill, outline, id, targetId) {
        super(id, targetId);
        this.color = color;
        this.fill = fill;
        this.outline = outline;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("fill", 'boolean', this.fill);
        kml += Kml.tag("outline", 'boolean', this.outline);
        return Kml.tag("PolyStyle", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<IconStyle id="ID">
  <!-- inherited from ColorStyle -->
  <color>ffffffff</color>            <!-- kml:color -->
  <colorMode>normal</colorMode>      <!-- kml:colorModeEnum:normal or random -->

  <!-- specific to IconStyle -->
  <scale>1</scale>                   <!-- float -->
  <heading>0</heading>               <!-- float -->
  <Icon>
    <href>...</href>
  </Icon>
  <hotSpot x="0.5"  y="0.5"
    xunits="fraction" yunits="fraction"/>    <!-- kml:vec2 -->
</IconStyle>
******************************************************************************************************************************************************************************************************/
class IconStyle extends ColorStyle {
    constructor(color, scale, iconHref, heading, id, targetId) {
        super(id, targetId);
        this.color = color;
        this.scale = scale;
        this.icon = new Icon();
        this.icon.href = iconHref;
        this.heading = heading;
    }
    setHotSpot(x, y, xunits, yunits) {
        this.hotSpot = new Vec2(x,y,xunits,yunits);
        return this;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("scale", 'float', this.scale);
        kml += Kml.tag("heading", 'float', this.heading);
        kml += this.icon.toKml();
        kml += Kml.tagVec2("hotSpot", this.hotSpot);
        return Kml.tag("IconStyle", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<LabelStyle id="ID">
  <!-- inherited from ColorStyle -->
  <color>ffffffff</color>            <!-- kml:color -->
  <colorMode>normal</colorMode>      <!-- kml:colorModeEnum: normal or random -->

  <!-- specific to LabelStyle -->
  <scale>1</scale>                   <!-- float -->
</LabelStyle>
******************************************************************************************************************************************************************************************************/
class LabelStyle extends ColorStyle {
    constructor(color, scale, id, targetId) {
        super(id, targetId);
        this.color = color;
        this.scale = scale;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("scale", 'float', this.scale);
        return Kml.tag("LabelStyle", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<Icon id="ID">
  <!-- specific to Icon -->
  <href>...</href>                         <!-- anyURI -->
  <gx:x>0<gx:x/>                           <!-- int -->
  <gx:y>0<gx:y/>                           <!-- int -->
  <gx:w>-1<gx:w/>                          <!-- int -->
  <gx:h>-1<gx:h/>                          <!-- int -->
  <refreshMode>onChange</refreshMode>
    <!-- kml:refreshModeEnum: onChange, onInterval, or onExpire -->
  <refreshInterval>4</refreshInterval>     <!-- float -->
  <viewRefreshMode>never</viewRefreshMode>
    <!-- kml:viewRefreshModeEnum: never, onStop, onRequest, onRegion -->
  <viewRefreshTime>4</viewRefreshTime>     <!-- float -->
  <viewBoundScale>1</viewBoundScale>       <!-- float -->
  <viewFormat>...</viewFormat>             <!-- string -->
  <httpQuery>...</httpQuery>               <!-- string -->
</Icon>
******************************************************************************************************************************************************************************************************/
class Icon extends KmlObject {
    constructor(href, id, targetId) {
        super(id, targetId);
        this.href = href;
    }
    setXY(x, y) {
        this.x = x;
        this.y = y;
        return this;
    }
    setWH(w, h) {
        this.w = w;
        this.h = h;
        return this;
    }
    setRefresh(refreshMode, refreshInterval) {
        this.refreshMode = refreshMode;
        this.refreshInterval = refreshInterval;
        return this;
    }
    setViewRefresh(viewRefreshMode, viewRefreshTime) {
        this.viewRefreshMode = viewRefreshMode;
        this.viewRefreshTime = viewRefreshTime;
        return this;
    }
    toKml() {
        let kml = Kml.tag("href", 'uri', this.href);
        kml += Kml.tag("x", 'int', this.x);
        kml += Kml.tag("y", 'int', this.y);
        kml += Kml.tag("w", 'int', this.w);
        kml += Kml.tag("h", 'int', this.h);
        kml += Kml.tag("refreshMode", 'refreshModeEnum', this.refreshMode);
        kml += Kml.tag("refreshInterval", 'float', this.refreshInterval);
        kml += Kml.tag("viewRefreshMode", 'viewRefreshModeEnum', this.viewRefreshMode);
        kml += Kml.tag("viewRefreshTime", 'float', this.viewRefreshTime);
        kml += Kml.tag("viewBoundScale", 'float', this.viewBoundScale);
        kml += Kml.tag("viewFormat", 'string', this.viewFormat);
        kml += Kml.tag("httpQuery", 'string', this.httpQuery);
        return Kml.tag("Icon", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<!-- abstract element; do not create -->
<!-- Overlay id="ID" -->                    <!-- GroundOverlay,ScreenOverlay -->
  <!-- inherited from Feature element -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
  <atom:link href=" "/>            <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>      <!-- new in KML 2.2 -->

  <!-- specific to Overlay -->
  <color>ffffffff</color>                   <!-- kml:color -->
  <drawOrder>0</drawOrder>                  <!-- int -->
  <Icon>
    <href>...</href>
  </Icon>
<!-- /Overlay -->
******************************************************************************************************************************************************************************************************/
class Overlay extends Feature {
    constructor(name, iconHref, id, targetId) {
        super(name, id, targetId);
        this.icon = new Icon(iconHref);
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("color", 'color', this.color);
        kml += Kml.tag("drawOrder", 'int', this.drawOrder);
        kml += this.icon.toKml();
        return kml;
    }
}
/*******************************************************************************************************************************************************************************************************
<GroundOverlay id="ID">
  <!-- inherited from Feature element -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
  <atom:link href=" "/>                <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>      <!-- new in KML 2.2 -->

  <!-- inherited from Overlay element -->
  <color>ffffffff</color>                   <!-- kml:color -->
  <drawOrder>0</drawOrder>                  <!-- int -->
  <Icon>...</Icon>

  <!-- specific to GroundOverlay -->
  <altitude>0</altitude>                    <!-- double -->
  <altitudeMode>clampToGround</altitudeMode>
     <!-- kml:altitudeModeEnum: clampToGround or absolute -->
     <!-- or, substitute gx:altitudeMode: clampToSeaFloor or relativeToSeaFloor -->
  <LatLonBox>
    <north>...</north>                      <! kml:angle90 -->
    <south>...</south>                      <! kml:angle90 -->
    <east>...</east>                        <! kml:angle180 -->
    <west>...</west>                        <! kml:angle180 -->
    <rotation>0</rotation>                  <! kml:angle180 -->
  </LatLonBox>
  <gx:LatLonQuad>
    <coordinates>...</coordinates>          <!-- four lon,lat tuples -->
  </gx:LatLonQuad>
</GroundOverlay>
******************************************************************************************************************************************************************************************************/
class GroundOverlay extends Overlay {
    constructor(name, iconHref, id, targetId) {
        super(name, iconHref, id, targetId);
    }
    setLatLonBox(north, south, east, west, rotation) {
        this.latLonBox = new LatLonBox(north,south,east,west,rotation);
        return this;
    }
    setLatLonQuad(coordinates) {
        this.latLonQuad = new LatLonQuad(coordinates);
        return this;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("altitude", 'double', this.altitude);
        kml += Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        if (typeof this.latLonBox !== 'undefined' && this.latLonBox != null )
            kml += this.latLonBox.toKml();
        if (typeof this.latLonQuad !== 'undefined' && this.latLonQuad != null )
            kml += this.latLonQuad.toKml();
        return Kml.tag("GroundOverlay", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<LatLonBox>
   <north>48.25475939255556</north>
   <south>48.25207367852141</south>
   <east>-90.86591508839973</east>
   <west>-90.8714285289695</west>
   <rotation>39.37878630116985</rotation>
</LatLonBox>
 ******************************************************************************************************************************************************************************************************/
class LatLonBox {
    constructor(north, south, east, west, rotation) {
        this.north = north;
        this.south = south;
        this.east = east;
        this.west = west;
        this.rotation = rotation;
    }
    toKml() {
        let kml = Kml.tag("north", 'angle90', this.north);
        kml += Kml.tag("south", 'angle90', this.south);
        kml += Kml.tag("east", 'angle180', this.east);
        kml += Kml.tag("west", 'angle180', this.west);
        kml += Kml.tag("rotation", 'angle180', this.rotation);
        return Kml.tag("LatLonBox", 'xml', kml);
    }
}
/*******************************************************************************************************************************************************************************************************
 <gx:LatLonQuad>
    <coordinates>...</coordinates>              <!-- four lon,lat tuples -->
  </gx:LatLonQuad>
 ******************************************************************************************************************************************************************************************************/
class LatLonQuad {
    constructor(coordinates) {
        this.coordinates = coordinates;
    }
    toKml() {
        let kml = "";
        if (this.coordinates.length !== 4)
            console.log("Warning: incorrect number of coordinates in LatLongQuad");
        kml = this.coordinates.reduce((p, c)=>p+coordinate.lng+","+coordinate.lat+" ", kml);
        return Kml.tag("gx:LatLonQuad", 'xml', Kml.tag("coordinates", 'coordinates', kml));
    }
}
/*******************************************************************************************************************************************************************************************************
<ScreenOverlay id="ID">
  <!-- inherited from Feature element -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
  <atom:link href=" "/>                <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>      <!-- new in KML 2.2 -->

  <!-- inherited from Overlay element -->
  <color>ffffffff</color>                  <!-- kml:color -->
  <drawOrder>0</drawOrder>                 <!-- int -->
  <Icon>...</Icon>

  <!-- specific to ScreenOverlay -->
  <overlayXY x="double" y="double" xunits="fraction" yunits="fraction"/>
    <!-- vec2 -->
    <!-- xunits and yunits can be one of: fraction, pixels, or insetPixels -->
  <screenXY x="double" y="double" xunits="fraction" yunits="fraction"/>
    <!-- vec2 -->
  <rotationXY x="double" y="double" xunits="fraction" yunits"fraction"/>
    <!-- vec2 -->
  <size x="double" y="double" xunits="fraction" yunits="fraction"/>
    <!-- vec2 -->
  <rotation>0</rotation>                   <!-- float -->
 </ScreenOverlay>
 ******************************************************************************************************************************************************************************************************/
class ScreenOverlay extends Overlay {
    constructor(name, iconHref, id, targetId) {
        super(name, iconHref, id, targetId);
    }
    setOverlayXY(x, y, xunits, yunits) {
        this.overlayXY = new Vec2(x,y,xunits,yunits);
        return this;
    }
    setScreenXY(x, y, xunits, yunits) {
        this.screenXY = new Vec2(x,y,xunits,yunits);
        return this;
    }
    setRotationXY(x, y, xunits, yunits) {
        this.rotationXY = new Vec2(x,y,xunits,yunits);
        return this;
    }
    setSize(x, y, xunits, yunits) {
        this.size = new Vec2(x,y,xunits,yunits);
        return this;
    }
    setRotation(rotation) {
        this.rotation = rotation;
        return this;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tagVec2("overlayXY", this.overlayXY);
        kml += Kml.tagVec2("screenXY", this.screenXY);
        kml += Kml.tagVec2("rotationXY", this.rotationXY);
        kml += Kml.tagVec2("size", this.size);
        kml += Kml.tag("rotation", 'float', this.rotation);
        return Kml.tag("ScreenOverlay", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}

class Vec2 {
    constructor(x, y, xunits, yunits) {
        xunits = xunits || "fraction";
        yunits = yunits || "fraction";
        this.x = x;
        this.y = y;
        this.xunits = xunits;
        this.yunits = yunits;
    }
}


/*******************************************************************************************************************************************************************************************************
<PhotoOverlay>
  <!-- inherited from Feature element -->
  <name>...</name>                      <!-- string -->
  <visibility>1</visibility>            <!-- boolean -->
  <open>0</open>                        <!-- boolean -->
  <atom:author>...<atom:author>         <!-- xmlns:atom -->
  <atom:link href=" "/>            <!-- xmlns:atom -->
  <address>...</address>                <!-- string -->
  <xal:AddressDetails>...</xal:AddressDetails>  <!-- xmlns:xal -->
  <phoneNumber>...</phoneNumber>        <!-- string -->
  <Snippet maxLines="2">...</Snippet>   <!-- string -->
  <description>...</description>        <!-- string -->
  <AbstractView>...</AbstractView>      <!-- Camera or LookAt -->
  <TimePrimitive>...</TimePrimitive>
  <styleUrl>...</styleUrl>              <!-- anyURI -->
  <StyleSelector>...</StyleSelector>
  <Region>...</Region>
  <Metadata>...</Metadata>              <!-- deprecated in KML 2.2 -->
  <ExtendedData>...</ExtendedData>      <!-- new in KML 2.2 -->

  <!-- inherited from Overlay element -->
  <color>ffffffff</color>               <!-- kml:color -->
  <drawOrder>0</drawOrder>              <!-- int -->
  <Icon>
    <href>...</href>                    <!-- anyURI -->
    ...
  </Icon>

  <!-- specific to PhotoOverlay -->
  <rotation>0</rotation>                <!-- kml:angle180 -->
  <ViewVolume>
    <leftFov>0</leftFov>                <!-- kml:angle180 -->
    <rightFov>0</rightFov>              <!-- kml:angle180 -->
    <bottomFov>0</bottomFov>            <!-- kml:angle90 -->
    <topFov>0</topFov>                  <!-- kml:angle90 -->
    <near>0</near>                      <!-- double -->
  </ViewVolume>
  <ImagePyramid>
    <tileSize>256</tileSize>            <!-- int -->
    <maxWidth>...</maxWidth>            <!-- int -->
    <maxHeight>...</maxHeight>          <!-- int -->
    <gridOrigin>lowerLeft</gridOrigin> <!-- lowerLeft or upperLeft -->
  </ImagePyramid>
  <Point>
    <coordinates>...</coordinates>      <!-- lon,lat[,alt] -->
  </Point>
  <shape>rectangle</shape>               <!-- kml:shape -->
</PhotoOverlay>
******************************************************************************************************************************************************************************************************/
class PhotoOverlay extends Overlay {
    constructor(name, iconHref, abstractView, point, id, targetId) {
        super(name, iconHref, id, targetId);
        this.abstractView = abstractView;
        this.point = point;
    }
    setViewVolume(near, leftFov, rightFov, bottomFov, topFov) {
        this.viewVolume = new ViewVolume(near,leftFov,rightFov,bottomFov,topFov);
        return this;
    }
    setImagePyramid(tileSize, maxWidth, maxHeight, gridOrigin) {
        this.imagePyramid = new ImagePyramid(tileSize,maxWidth,maxHeight,gridOrigin);
        return this;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("rotation", 'angle180', this.rotation);
        if (!isEmpty(this.viewVolume)) {
            kml += this.viewVolume.toKml()
        }
        if (!isEmpty(this.imagePyramid)) {
            kml += this.imagePyramid.toKml()
        }
        if (!isEmpty(this.point)) {
            kml += this.point.toKml();
        }
        //shape=rectangle,cylinder,sphere
        kml += Kml.tag("shape", 'shapeEnum', this.shape);
        return Kml.tag("PhotoOverlay", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}

class ViewVolume {
    constructor(near, leftFov, rightFov, bottomFov, topFov) {
        this.near = near;
        this.leftFov = leftFov;
        this.rightFov = rightFov;
        this.bottomFov = bottomFov;
        this.topFov = topFov;
    }
    toKml() {
        let kml = Kml.tag("leftFov", 'angle180', this.leftFov);
        kml += Kml.tag("rightFov", 'angle180', this.rightFov);
        kml += Kml.tag("bottomFov", 'angle90', this.bottomFov);
        kml += Kml.tag("topFov", 'angle90', this.topFov);
        return Kml.tag("ViewVolume", 'xml', kml);
    }
}

class ImagePyramid {
    constructor(tileSize, maxWidth, maxHeight, gridOrigin) {
        this.tileSize = tileSize;
        this.maxWidth = maxWidth;
        this.maxHeight = maxHeight;
        this.gridOrigin = gridOrigin;
    }
    toKml() {
        let kml = Kml.tag("tileSize", 'int', this.tileSize);
        kml += Kml.tag("maxWidth", 'int', this.maxWidth);
        kml += Kml.tag("maxHeight", 'int', this.maxHeight);
        kml += Kml.tag("gridOrigin", 'gridOrigin', this.gridOrigin);
        return Kml.tag("ImagePyramid", 'xml', kml);
    }
}



/*******************************************************************************************************************************************************************************************************
<!-- abstract element; do not create -->
<!-- AbstractView -->                       <!-- Camera, LookAt -->
  <!-- extends Object -->
  <TimePrimitive>...</TimePrimitive>        <!-- gx:TimeSpan or gx:TimeStamp -->
  <gx:ViewerOptions>
    <gx:option name="" enabled=boolean />   <!-- name="streetview",
                                                      "historicalimagery",
                                                   or "sunlight" -->
  </gx:ViewerOptions>
<-- /AbstractView -->
******************************************************************************************************************************************************************************************************/
class AbstractView extends KmlObject {
    constructor(id, targetId) {
        super(id, targetId);
    }
    setTimeStamp(when) {
        this.timePrimitive = new TimePrimitive('timeStamp',when);
        return this;
    }
    setTimeSpan(begin, end) {
        this.timePrimitive = new TimePrimitive('timeSpan',begin,end);
        return this;
    }
    addViewerOption(name, enabled) {
        enabled = enabled || "1";
        if (typeof this.viewerOptions === 'undefined') {
            this.viewerOptions = new ViewerOptions();
        }
        this.viewerOptions.options.push({
            name: name,
            enabled: enabled
        });
    }
    toKml() {
        let kml = "";
        if (typeof this.timePrimitive !== 'undefined' && this.timePrimitive != null  && this.timePrimitive != "") {
            kml += this.timePrimitive.toKml();
        }
        if (typeof this.viewerOptions !== 'undefined') {
            kml += this.viewerOptions.toKml();
        }
        return kml;
    }
}
/*******************************************************************************************************************************************************************************************************
  <gx:ViewerOptions>
    <gx:option name="" enabled=boolean />   <!-- name="streetview",
                                                      "historicalimagery",
                                                   or "sunlight" -->
  </gx:ViewerOptions>
******************************************************************************************************************************************************************************************************/
class ViewerOptions {
    constructor() {
        this.options = [];
    }
    toKml() {
        let kml = "";
        for (let i = 0; i < this.options.length; i += 1) {
            kml += Kml.tag("gx:option", 'string', "", {
                name: this.options[i].name,
                enabled: this.options[i].enabled
            }, true);
        }
        return Kml.tag("gx:ViewerOptions", 'xml', kml);
    }
}

/*******************************************************************************************************************************************************************************************************
<TimePrimitive>...</TimePrimitive>        <!-- gx:TimeSpan or gx:TimeStamp -->
******************************************************************************************************************************************************************************************************/
class TimePrimitive {
    constructor(type, first, second) {
        if (type === 'timeStamp') {
            this.when = TimePrimitive.convertDate(first);
        }
        if (type === 'timeSpan') {
            this.begin = TimePrimitive.convertDate(first);
            this.end = TimePrimitive.convertDate(second);
        }
    }
    static convertDate(date) {
        if (typeof date === 'string') {
            return date;
        } else if (date instanceof Date) {
            return date.toISOString();
        }
        console.log("Warning: invalid TimePrimitive");
        return "";
    }
    toKml() {
        if (typeof this.when !== 'undefined' && this.when !== null  && this.when !== "") {
            let kml = Kml.tag("when", 'dateTime', this.when);
            return Kml.tag("gx:TimeStamp", 'xml', kml);
        }
        else if ((typeof this.begin !== 'undefined' && this.begin !== null  && this.begin !== "") || (typeof this.end !== 'undefined' && this.end !== null  && this.end !== "")) {
            let kml = Kml.tag("begin", 'dateTime', this.begin);
            kml += Kml.tag("end", 'dateTime', this.end);
            return Kml.tag("gx:TimeSpan", 'xml', kml);
        }
        console.log(`Warning: Empty time primitive.`)
        return "";
    }
}
/*******************************************************************************************************************************************************************************************************
<Camera id="ID">
  <!-- inherited from AbstractView element -->
  <TimePrimitive>...</TimePrimitive>  <!-- gx:TimeSpan or gx:TimeStamp -->
  <gx:ViewerOptions>
    <option> name=" " type="boolean">     <!-- name="streetview", "historicalimagery", "sunlight", or "groundnavigation" -->
    </option>
  </gx:ViewerOptions>

  <!-- specific to Camera -->
  <longitude>0</longitude>            <!-- kml:angle180 -->
  <latitude>0</latitude>              <!-- kml:angle90 -->
  <altitude>0</altitude>              <!-- double -->
  <heading>0</heading>                <!-- kml:angle360 -->
  <tilt>0</tilt>                      <!-- kml:anglepos180 -->
  <roll>0</roll>                      <!-- kml:angle180 -->
  <altitudeMode>clampToGround</altitudeMode>
        <!-- kml:altitudeModeEnum: relativeToGround, clampToGround, or absolute -->
        <!-- or, gx:altitudeMode can be substituted: clampToSeaFloor, relativeToSeaFloor -->
</Camera>
******************************************************************************************************************************************************************************************************/
class Camera extends AbstractView {
    constructor(longitude, latitude, altitude, heading, tilt, roll, altitudeMode, id, targetId) {
        super(id, targetId);
        this.longitude = longitude;
        this.latitude = latitude;
        this.altitude = altitude;
        this.heading = heading
        this.tilt = tilt;
        this.roll = roll;
        this.altitudeMode = altitudeMode;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("longitude", 'angle180', this.longitude);
        kml += Kml.tag("latitude", 'angle90', this.latitude);
        kml += Kml.tag("altitude", 'double', this.altitude);
        kml += Kml.tag("heading", 'angle360', this.heading);
        kml += Kml.tag("tilt", 'anglepos180', this.tilt);
        kml += Kml.tag("roll", 'angle180', this.roll);
        kml += Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode)
        return Kml.tag("Camera", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<LookAt id="ID">
  <!-- inherited from AbstractView element -->
  <TimePrimitive>...</TimePrimitive>  <!-- gx:TimeSpan or gx:TimeStamp -->
  <gx:ViewerOptions>
    <option> name=" " type="boolean">     <!-- name="streetview", "historicalimagery", "sunlight", or "groundnavigation" -->
    </option>
  </gx:ViewerOptions>

  <!-- specific to LookAt -->
  <longitude>0</longitude>            <!-- kml:angle180 -->
  <latitude>0</latitude>              <!-- kml:angle90 -->
  <altitude>0</altitude>              <!-- double -->
  <heading>0</heading>                <!-- kml:angle360 -->
  <tilt>0</tilt>                      <!-- kml:anglepos90 -->
  <range></range>                     <!-- double -->
  <altitudeMode>clampToGround</altitudeMode>
          <!--kml:altitudeModeEnum:clampToGround, relativeToGround, absolute -->
          <!-- or, gx:altitudeMode can be substituted: clampToSeaFloor, relativeToSeaFloor -->

</LookAt>
******************************************************************************************************************************************************************************************************/
class LookAt extends AbstractView {
    constructor(longitude, latitude, altitude, heading, tilt, range, altitudeMode, id, targetId) {
        super(id, targetId);
        this.longitude = longitude;
        this.latitude = latitude;
        this.altitude = altitude;
        this.heading = heading
        this.tilt = tilt;
        // differs from camera on this field only
        this.range = range;
        this.altitudeMode = altitudeMode;
    }
    toKml() {
        let kml = super.toKml();
        kml += Kml.tag("longitude", 'angle180', this.longitude);
        kml += Kml.tag("latitude", 'angle90', this.latitude);
        kml += Kml.tag("altitude", 'double', this.altitude);
        kml += Kml.tag("heading", 'angle360', this.heading);
        kml += Kml.tag("tilt", 'anglepos90', this.tilt);
        kml += Kml.tag("range", 'double', this.range);
        kml += Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        return Kml.tag("LookAt", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:Tour id="ID">
  <name>...</name>
  <description>...</description>
  <gx:Playlist>

    <!-- any number of gx:TourPrimitive elements -->

  </gx:Playlist>
</gx:Tour>
******************************************************************************************************************************************************************************************************/
class Tour extends Feature {
    constructor(name, id, targetId) {
        super(name, id, targetId);
        this.playlist = new Playlist();
    }
    addTourPrimitive(tourPrimitive) {
        this.playlist.tourPrimitives.push(tourPrimitive);
        return this;
    }
    toKml() {
        let kml = Kml.tag("name", 'string', this.name);
        kml += Kml.tag("description", 'html', this.description);
        kml += this.playlist.toKml();
        return Kml.tag("gx:Tour", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/***********************************************************************
***********************************************************************/
class Playlist extends KmlObject {
    constructor(id, targetId) {
        super(id, targetId);
        this.tourPrimitives = [];
    }
    toKml() {
        let kml = this.tourPrimitives.reduce((p, c)=>p+c.toKml(), "")
        return Kml.tag("gx:Playlist", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:Tour>
  <gx:Playlist>

    <!-- abstract element; do not create -->
    <!-- gx:TourPrimitive -->    <!-- gx:AnimatedUpdate, gx:FlyTo, gx:TourControl, gx:SoundCue, gx:Wait -->
        <!-- extends Object -->
    <!-- /gx:TourPrimitive -->

  </gx:Playlist>
</gx:Tour>
******************************************************************************************************************************************************************************************************/
class TourPrimitive extends KmlObject {
    constructor(id, targetId) {
        super(id, targetId);
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:AnimatedUpdate id="ID">
  <gx:duration>0.0</gx:duration>     <!-- double, specifies time in seconds -->
  <Update>
    <targetHref>...</targetHref>     <!-- required; can contain a URL or be left blank -->
                                      <!-- (to target elements within the same file) -->
    <Change>...</Change>
    <Create>...</Create>
    <Delete>...</Delete>
  </Update>
  <gx:delayedStart>0</gx:delayedStart>  <!-- double, specifies time in seconds -->
</gx:AnimatedUpdate>
******************************************************************************************************************************************************************************************************/
class AnimatedUpdate extends TourPrimitive {
    constructor(duration, delayedStart, id, targetId) {
        super(id, targetId);
        this.duration = duration;
        this.delayedStart = delayedStart;
        this.update = new Update();
    }
    addChange(change) {
        if (isEmpty(this.update.change))
            this.update.change = new Change();
        this.update.change.changes.push(change);
        return this;
    }
    addCreate(create) {
        if (isEmpty(this.update.create))
            this.update.create = new Create();
        this.update.create.creates.push(create);
        return this;
    }
    addDelete(_delete) {
        if (isEmpty(this.update.delete))
            this.update.delete = new Delete();
        this.update.delete.deletes.push(_delete);
        return this;
    }
    toKml() {
        let kml = Kml.tag("gx:duration", 'double', this.duration);
        kml += Kml.tag("gx:delayedStart", 'double', this.delayedStart);
        kml += this.update.toKml();
        return Kml.tag("gx:AnimatedUpdate", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        }, true);
    }
}
/*******************************************************************************************************************************************************************************************************
<Update>
  <targetHref>...</targetHref>    <!-- URL -->
  <Change>...</Change>
  <Create>...</Create>
  <Delete>...</Delete>
</Update>
******************************************************************************************************************************************************************************************************/
class Update {
    constructor() {
        // required but typically blank
        this.targetHref = " ";
    }
    toKml() {
        this.targetHref = this.targetHref || " ";
        let kml = Kml.tag("targetHref", 'url', this.targetHref);
        if (!isEmpty(this.change))
            kml += this.change.toKml();
        if (!isEmpty(this.create))
            kml += this.create.toKml();
        if (!isEmpty(this.delete))
            kml += this.delete.toKml();
        return Kml.tag("Update", 'xml', kml);
    }
}
class Change {
    constructor() {
        this.changes = [];
    }
    toKml() {
        let kml = "";
        for (let i = 0; i < this.changes.length; i += 1)
            kml += this.changes[i].toKml();
        return Kml.tag("Change", 'xml', kml);
    }
}
class Create {
    constructor() {
        this.creates = [];
    }
    toKml() {
        let kml = "";
        for (let i = 0; i < this.creates.length; i += 1)
            kml += this.creates[i].toKml();
        return Kml.tag("Create", 'xml', kml);
    }

}
class Delete {
    constructor() {
        this.deletes = [];
    }
    toKml() {
        let kml = "";
        for (let i = 0; i < this.deletes.length; i += 1)
            kml += this.deletes[i].toKml();
        return Kml.tag("Delete", 'xml', kml);
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:FlyTo id="ID">
  <gx:duration>0.0</gx:duration>         <!-- double -->
  <gx:flyToMode>bounce</gx:flyToMode>    <!-- smooth or bounce -->
  <!-- AbstractView -->                        <!-- Camera or LookAt -->
    ...
  <!-- /AbstractView -->
</gx:FlyTo>
******************************************************************************************************************************************************************************************************/
class FlyTo extends TourPrimitive {
    constructor(duration, flyToMode, abstractView, id, targetId) {
        super(id);
        this.duration = duration;
        this.flyToMode = flyToMode;
        this.abstractView = abstractView;
    }
    toKml() {
        let kml = Kml.tag("gx:duration", 'double', this.duration);
        kml += Kml.tag("gx:flyToMode", 'flyToModeEnum', this.flyToMode);
        kml += this.abstractView.toKml();
        return Kml.tag("gx:FlyTo", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:SoundCue id="ID">
  <href>http://www.example.com/audio/trumpets.mp3</href>   <!-- any URI -->
  <gx:delayedStart>0</gx:delayedStart>                     <!-- double -->
</gx:SoundCue>
******************************************************************************************************************************************************************************************************/
class SoundCue extends TourPrimitive {
    constructor(href, delayedStart, id, targetId) {
        super(id);
        this.href = href;
        this.delayedStart = delayedStart;
    }
    toKml() {
        let kml = Kml.tag("href", 'uri', this.href);
        kml += Kml.tag("gx:delayedStart", 'double', this.delayedStart);
        return Kml.tag("gx:SoundCue", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:TourControl id="ID">
  <gx:playMode>pause</gx:playMode>    <!-- gx:playModeEnum: pause -->
</gx:TourControl>
******************************************************************************************************************************************************************************************************/
class TourControl extends TourPrimitive {
    constructor(id, targetId) {
        super(id);
        this.playMode = "pause";
    }
    toKml() {
        let kml = Kml.tag("gx:playMode", 'playModeEnum', this.playMode);
        return Kml.tag("gx:TourControl", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:Wait id="ID">
  <gx:duration>0.0</gx:duration>    <!-- double -->
</gx:Wait>
******************************************************************************************************************************************************************************************************/
class Wait extends TourPrimitive {
    constructor(duration, id, targetId) {
        super(id, targetId);
        this.duration = duration;
    }
    toKml() {
        let kml = Kml.tag("gx:duration", 'double', this.duration);
        return Kml.tag("gx:Wait", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<Region id="ID">
  <LatLonAltBox>
    <north></north>                            <!-- required; kml:angle90 -->
    <south></south>                            <!-- required; kml:angle90 -->
    <east></east>                              <!-- required; kml:angle180 -->
    <west></west>                              <!-- required; kml:angle180 -->
    <minAltitude>0</minAltitude>               <!-- float -->
    <maxAltitude>0</maxAltitude>               <!-- float -->
    <altitudeMode>clampToGround</altitudeMode>
        <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
        <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
  </LatLonAltBox>
  <Lod>
    <minLodPixels>0</minLodPixels>             <!-- float -->
    <maxLodPixels>-1</maxLodPixels>            <!-- float -->
    <minFadeExtent>0</minFadeExtent>           <!-- float -->
    <maxFadeExtent>0</maxFadeExtent>           <!-- float -->
  </Lod>
</Region>
******************************************************************************************************************************************************************************************************/
class Region extends KmlObject {
    constructor(id, targetId) {
        super(id, targetId);
    }
    setLatLonAltBox(north, south, east, west, minAltitude, maxAltitude, altitudeMode) {
        this.latLonAltBox = new LatLonAltBox(north,south,east,west,minAltitude,maxAltitude,altitudeMode);
        return this;
    }
    setLod(minLodPixels, maxLodPixels, minFadeExtent, maxFadeExtent) {
        this.lod = new Lod(minLodPixels,maxLodPixels,minFadeExtent,maxFadeExtent);
        return this;
    }
    toKml() {
        let kml = "";
        if (!isEmpty(this.latLonAltBox)) {
            kml += this.latLonAltBox.toKml();
        }
        if (!isEmpty(this.lod)) {
            kml += this.lod.toKml();
        }
        return Kml.tag("Region", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<LatLonAltBox>
    <north></north>                            <!-- required; kml:angle90 -->
    <south></south>                            <!-- required; kml:angle90 -->
    <east></east>                              <!-- required; kml:angle180 -->
    <west></west>                              <!-- required; kml:angle180 -->
    <minAltitude>0</minAltitude>               <!-- float -->
    <maxAltitude>0</maxAltitude>               <!-- float -->
    <altitudeMode>clampToGround</altitudeMode>
        <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
        <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
  </LatLonAltBox>
******************************************************************************************************************************************************************************************************/
class LatLonAltBox {
    constructor(north, south, east, west, minAltitude, maxAltitude, altitudeMode) {
        this.north = north;
        this.south = south;
        this.east = east;
        this.west = west;
        this.minAltitude = minAltitude;
        this.maxAltitude = maxAltitude;
        this.altitudeMode = altitudeMode;
    }
    toKml() {
        let kml = Kml.tag("north", 'angle90', this.north);
        kml += Kml.tag("south", 'angle90', this.south);
        kml += Kml.tag("east", 'angle180', this.east);
        kml += Kml.tag("west", 'angle180', this.west);
        kml += Kml.tag("minAltitude", 'float', this.minAltitude);
        kml += Kml.tag("maxAltitude", 'float', this.maxAltitude);
        kml += Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        return Kml.tag("LatLonAltBox", 'xml', kml);
    }

}
/*******************************************************************************************************************************************************************************************************
<Lod>
    <minLodPixels>0</minLodPixels>             <!-- float -->
    <maxLodPixels>-1</maxLodPixels>            <!-- float -->
    <minFadeExtent>0</minFadeExtent>           <!-- float -->
    <maxFadeExtent>0</maxFadeExtent>           <!-- float -->
  </Lod>
******************************************************************************************************************************************************************************************************/
class Lod {
    constructor(minLodPixels, maxLodPixels, minFadeExtent, maxFadeExtent) {
        this.minLodPixels = minLodPixels;
        this.maxLodPixels = maxLodPixels;
        this.minFadeExtent = minFadeExtent;
        this.maxFadeExtent = maxFadeExtent;
    }
    toKml() {
        let kml = Kml.tag("minLodPixels", 'float', this.minLodPixels);
        kml += Kml.tag("maxLodPixels", 'float', this.maxLodPixels);
        kml += Kml.tag("minFadeExtent", 'float', this.minFadeExtent);
        kml += Kml.tag("maxFadeExtent", 'float', this.maxFadeExtent);
        return Kml.tag("Lod", 'xml', kml);
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:Track id="ID">
<!-- specific to Track -->
<altitudeMode>clampToGround</altitudeMode>
    <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
    <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
<when>...</when>                         <!-- kml:dateTime -->
<gx:coord>...</gx:coord>                 <!-- string -->
<gx:angles>...</gx:angles>               <!-- string -->
<Model>...</Model>
<ExtendedData>
  <SchemaData schemaUrl="anyURI">
    <gx:SimpleArrayData kml:name="string">
      <gx:value>...</gx:value>            <!-- string -->
    </gx:SimpleArrayData>
  <SchemaData>
</ExtendedData>
</gx:Track>
******************************************************************************************************************************************************************************************************/
class Track extends KmlObject {
    constructor(id, targetId) {
        super(id, targetId);
        this.whens = [];
        this.coords = [];
        this.angles = [];
    }
    addWhen(when) {
        this.whens.push(TimePrimitive.convertDate(when));
        return this;
    }
    //pass a Coordinate object
    addCoord(coord) {
        this.coords.push(coord);
        return this;
    }
    addAngle(heading, tilt, roll) {
        let angle = {
            heading,
            tilt,
            roll
        };
        this.angles.push(angle);
        return this;
    }
    toKml() {
        let kml = Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        kml = this.whens.reduce((p, c)=>p+Kml.tag("when", 'dateTime', c), kml);
        kml = this.coords.reduce((p, c)=>p+Kml.tag("gx:coord", 'string', c.lng+" "+c.lat+" "+c.alt), kml);
        kml = this.angles.reduce((p, c)=>p+Kml.tag("gx:angles", 'string', c.heading+" "+c.tilt+" "+c.roll), kml);
        if (!isEmpty(this.model))
            kml += this.model.toKml();
        if (!isEmpty(this.extendedData))
            kml += this.extendedData.toKml();
        return Kml.tag("Track", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
<gx:MultiTrack id="ID">
  <!-- specific to MultiTrack -->
  <altitudeMode>clampToGround</altitudeMode>
        <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
        <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
  <gx:interpolate>0<gx:interpolate>   <!-- boolean -->
  <gx:Track>...</gx:Track>            <!-- one or more gx:Track elements -->
</gx:MultiTrack>
******************************************************************************************************************************************************************************************************/
class MultiTrack extends Geometry {
    constructor(id, targetId) {
        super(id, targetId);
        this.tracks = [];
    }
    toKml() {
        let kml = Kml.tag("altitudeMode", 'altitudeModeEnum', this.altitudeMode);
        kml += Kml.tag("gx:interpolate", 'boolean', this.interpolate)
        for (let i = 0; i < this.tracks.length; i += 1)
            kml += this.tracks[i].toKml();
        return Kml.tag("MultiTrack", 'xml', kml, {
            id: this.id,
            targetId: this.targetId
        });
    }
}
/*******************************************************************************************************************************************************************************************************
 * Not a true KML class
 ******************************************************************************************************************************************************************************************************/

class Coordinate {
    constructor(lat, lng, alt) {
        if (!isEmpty(lat) && !isNaN(lat)) {
            this.lat = parseFloat(lat);
        } else {
            this.lat = 0;
        }
        if (!isEmpty(lng) && !isNaN(lng)) {
            this.lng = parseFloat(lng);
        } else {
            this.lng = 0;
        }
        if (!isEmpty(alt) && !isNaN(alt)) {
            this.alt = parseFloat(alt);
        } else {
            this.alt = 0;
        }
    }
    toKml() {
        return this.lng + "," + this.lat + "," + (altitude_decimals ? this.alt : this.alt.toFixed()) + " ";
    }
    clone(p2) {
        this.lat = p2.lat;
        this.lng = p2.lng;
        this.alt = p2.alt;
    }

    /***************************************************************************************************************************************************************************************************
	 * Tools for distance and arcs
	 **************************************************************************************************************************************************************************************************/
    /*
    * Dependancy:GeographicLib
    * http://geographiclib.sourceforge.net/1.45/js/
    */
    distanceTo(p2) {
        const geod = GeographicLib.Geodesic.WGS84;
        let r = geod.Inverse(this.lat, this.lng, p2.lat, p2.lng);
        return r.s12;
    }
    bearingTo(p2) {
        const Geodesic = GeographicLib.Geodesic;
        const geod = Geodesic.WGS84;
        let r = geod.Inverse(this.lat, this.lng, p2.lat, p2.lng, Geodesic.AZIMUTH)
        let azimuth = r.azi1;
        while (azimuth < 0) {
            azimuth += 360;
        }
        return azimuth;
    }
    destinationPoint(azimuth, distance) {
        const Geodesic = GeographicLib.Geodesic;
        const geod = Geodesic.WGS84;
        let r = geod.Direct(this.lat, this.lng, azimuth, distance, Geodesic.LATITUDE | Geodesic.LONGITUDE);
        return new Coordinate(r.lat2,r.lon2);
    }
    // Haversine formula from: http://stackoverflow.com/questions/1502590/calculate-distance-between-two-points-in-google-maps-v3
    distanceToOld(p2) {
        // Earth鈥檚 mean radius in metres
        let R = 6378137;
        let dLat = (p2.lat - this.lat).toRadians();
        let dLong = (p2.lng - this.lng).toRadians();
        let a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(this.lat.toRadians()) * Math.cos(p2.lat.toRadians()) * Math.sin(dLong / 2) * Math.sin(dLong / 2);
        let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        let d = R * c;
        // returns the distance in metres
        return d;
    }
    // http://www.movable-type.co.uk/scripts/latlong.html
    distanceToGreatCircle(p1, p2) {
        return Math.abs(this.distanceToGreatCircleSigned(p1, p2));
    }
    //sign indicates which side of line.
    distanceToGreatCircleSigned(p1, p2) {
        // point 3 is 'this'
        let R = 6378137;
        let d13 = p1.distanceTo(this);
        let theta13 = p1.bearingTo(this).toRadians();
        let theta12 = p1.bearingTo(p2).toRadians();
        let dXt = Math.asin(Math.sin(d13 / R) * Math.sin(theta13 - theta12)) * R;
        return dXt;
    }

    // Formula: dxt = asin( sin(delta13) 鈰� sin(theta13鈭抰heta12) ) 鈰� R
    // where delta13 is (angular) distance from start point to third point
    // theta13 is (initial) bearing from start point to third point
    // theta12 is (initial) bearing from start point to end point
    // R is the earth鈥檚 radius
    // JavaScript:
    // let dXt = Math.asin(Math.sin(d13/R)*Math.sin(theta13-theta12)) * R;

    equals(p2) {
        return ( this.lat === p2.lat && this.lng === p2.lng && this.alt === p2.alt) ;
    }
    // is the point within sensitivity metres (ignores altitude)
    near(p2, sensitivity) {
        return this.distanceTo(p2) <= sensitivity;
    }

    //     isOnGreatCircleSegment(p1, p2, sensitivity) {
    //         // should not be close to end points
    //         if (this.near(p1, sensitivity) || this.near(p2, sensitivity))
    //             return false;
    //         let segmentLength = p1.distanceTo(p2);
    //         if (this.distanceTo(p1) <= segmentLength && this.distanceTo(p2) <= segmentLength) {
    //             return this.distanceToGreatCircle(p1, p2) <= sensitivity;
    //         }
    //         return false;
    //     }

    isOnGreatCircleSegment(p1, p2) {
        let s12 = p1.distanceTo(p2);
        let s13 = p1.distanceTo(this);
        let s23 = p2.distanceTo(this);
        return s13 * s13 < s12 * s12 + s23 * s23 && s23 * s23 < s12 * s12 + s13 * s13;
    }
    findClosestPoint(points) {
        let distances = points.map(point=>this.distanceTo(point));
        let minDistance = Math.min(...distances);
        return {
            i: distances.findIndex(distance=>distance===minDistance),
            distance: minDistance
        }
    }
    findClosestSegment(points) {
        let segments = Coordinate.toSegments(points);
        let validSegments = segments.filter(segment=>this.isOnGreatCircleSegment(segment[0], segment[1]));
        if (validSegments.length === 0) {
            return {
                i: -1
            };
        }
        let distances = validSegments.map(segment=>this.distanceToGreatCircle(segment[0], segment[1]));
        let minDistance = Math.min(...distances);
        let closestSegment = validSegments[distances.findIndex(distance=>distance===minDistance)];
        return {
            i: segments.findIndex(segment=>segment[0].equals(closestSegment[0])&&segment[1].equals(closestSegment[1])),
            distance: minDistance
        }
    }
    createArcTo(p2, divisions, altitudeMethod, maxAlt) {
        let arc = [];
        arc.push(this);
        switch (altitudeMethod) {
        case "fixed":
            break;
        case "automatic":
        default:
            maxAlt = Math.sqrt(this.distanceTo(p2)) * 40;
            break;
        }
        for (let i = 1; i < divisions; i += 1) {
            let fraction = i / divisions;
            let point = this.intermediatePoint(p2, fraction);
            point.alt = this.intermediateAltitude(p2, fraction, maxAlt);
            arc.push(point);
        }
        arc.push(p2);
        return arc;
    }
    static toSegments(coordinates) {
        return coordinates.map((coordinate, i)=>[coordinate, coordinates[i<coordinates.length-1?i+1:0]]);
    }
    intermediateAltitude(p2, f, maxAlt) {
        return Math.round(Math.sin(f * Math.PI) * maxAlt + Math.abs(this.alt - p2.alt) * ((this.alt <= p2.alt) ? f : 1 - f) + Math.min(this.alt, p2.alt));
    }

    /* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
    /* http://williams.best.vwh.net/avform.htm#Intermediate */
    /* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
    intermediatePoint(p2, f) {
        let phi1 = this.lat.toRadians();
        let lambda1 = this.lng.toRadians();
        let phi2 = p2.lat.toRadians();
        let lambda2 = p2.lng.toRadians();
        let deltaphi = (p2.lat - this.lat).toRadians();
        let deltalambda = (p2.lng - this.lng).toRadians();
        let alpha = Math.sin(deltaphi / 2) * Math.sin(deltaphi / 2) + Math.cos(phi1) * Math.cos(phi2) * Math.sin(deltalambda / 2) * Math.sin(deltalambda / 2);
        let delta = 2 * Math.atan2(Math.sqrt(alpha), Math.sqrt(1 - alpha));
        let a = Math.sin((1 - f) * delta) / Math.sin(delta)
        let b = Math.sin(f * delta) / Math.sin(delta);
        let x = a * Math.cos(phi1) * Math.cos(lambda1) + b * Math.cos(phi2) * Math.cos(lambda2);
        let y = a * Math.cos(phi1) * Math.sin(lambda1) + b * Math.cos(phi2) * Math.sin(lambda2);
        let z = a * Math.sin(phi1) + b * Math.sin(phi2);
        let latRad = Math.atan2(z, Math.sqrt(x * x + y * y));
        let lngRad = Math.atan2(y, x);
        return new Coordinate(latRad.toDegrees(),lngRad.toDegrees());
    }



    bearingToOld(p2) {
        let phi1 = this.lat.toRadians();
        let lambda1 = this.lng.toRadians();
        let phi2 = p2.lat.toRadians();
        let lambda2 = p2.lng.toRadians();
        let y = Math.sin(lambda2 - lambda1) * Math.cos(phi2);
        let x = Math.cos(phi1) * Math.sin(phi2) - Math.sin(phi1) * Math.cos(phi2) * Math.cos(lambda2 - lambda1);
        let bearing = Math.atan2(y, x).toDegrees();
        return (bearing + 360) % 360;
    }
}

/** Extend Number object with method to convert numeric degrees to radians */
if (Number.prototype.toRadians === undefined) {
    Number.prototype.toRadians = function() {
        return this * Math.PI / 180;
    }
    ;
}
/**
 * Extend Number object with method to convert radians to numeric (signed) degrees
 */
if (Number.prototype.toDegrees === undefined) {
    Number.prototype.toDegrees = function() {
        return this * 180 / Math.PI;
    }
    ;
}


/*******************************************************************************************************************************************************************************************************
 * Tools for working with files
 ******************************************************************************************************************************************************************************************************/


/*
* Dependancy:FileSaver.min.js
* https://github.com/eligrey/FileSaver.js/
*/
function download(filename, text) {
    let blob = new Blob([text],{
        type: "text/plain"
    });
    saveAs(blob, filename);
}

/*
* Dependancy:jQuery
*/
function readAsKml(fileControl, complete) {
    // Check for the various File API support.
    if (window.File && window.FileReader && window.FileList && window.Blob) {
    // Great success! All the File APIs are supported.
    } else
        alert('The File APIs are not fully supported in this browser.');
    let files = fileControl.files;
    if (files.length === 0) {
        alert("Please select a file");
        return;
    }
    let coordsArrays = [];
    coordsArrays.filenames = "";
    // Loop through the FileList and render image files as thumbnails.
    for (let i = 0, j = 0, f; f = files[i]; i += 1) {
        let reader = new FileReader();
        // Closure to capture the file information.
        reader.onload = (function(theFile) {
            return function(e) {
                coordsArrays.filenames += theFile.name.slice(0, -4) + " ";
                if (theFile.name.slice(-4) === ".kml")
                    readKml(e.target.result, coordsArrays, theFile.name);
                else if (theFile.name.slice(-4) === ".kmz") {
                    let zip = new JSZip(e.target.result);
                    // for(let entryName in zip.files)
                    jQuery.each(zip.files, function(index, zipEntry) {
                        if (zipEntry.name.slice(-4) === ".kml")
                            readKml(zipEntry.asText(), coordsArrays, zipEntry.name);
                        else
                            console.log("Non-KML file found in KMZ:" + zipEntry.name);
                    });
                }
                j++;
                if (j === files.length)
                    complete(coordsArrays);
            }
        })(f);
        if (f.name.slice(-4) === ".kml")
            reader.readAsText(f, "UTF-8");
        else if (f.name.slice(-4) === ".kmz")
            reader.readAsArrayBuffer(f);
        else
            alert("Unknown file type:" + f.name);
    }
}

/*
Dependancy:jQuery
*/
function readKml(kmlString, coordsArrays, filename) {
    if (document.getElementById('outputErrors') != null  && document.getElementById('outputErrors').checked)
        correctedString = kmlString;
    let xmlDoc = jQuery.parseXML(kmlString);
    let xml = jQuery(xmlDoc);
    xml.find('Placemark').each(function(index) {
        let name = jQuery(this).find("name").text();
        jQuery(this).find('Point').each(function(index) {
            coordsArrays.push(coordsStringToArray(jQuery(this).find('coordinates').text(), "Point", name, filename));
        }
        );
        jQuery(this).find('Polygon').each(function(index) {
            coordsArrays.push(coordsStringToArray(jQuery(this).find('coordinates').text(), "Polygon", name, filename));
        }
        );
        jQuery(this).find('LineString').each(function(index) {
            coordsArrays.push(coordsStringToArray(jQuery(this).find('coordinates').text(), "LineString", name, filename));
        }
        );
    }
    );
}

function coordsStringToArray(polyCoordsString, type, name, filename) {
    let coords = (" " + polyCoordsString).match(/\S+/g);
    let coordsArray = [];
    for (let i = 0; i < coords.length; i += 1) {
        let coord = coords[i].split(",");
        if (!isEmpty(coord[0]) && !isNaN(coord[0]) && parseFloat(coord[0]) !== undefined) {
            coordsArray.push(new Coordinate(coord[1],coord[0],coord[2]));
            if (coordsArray.length > 2 && coordsArray[coordsArray.length - 1].equals(coordsArray[coordsArray.length - 2])) {
                let duplicate = coordsArray[coordsArray.length - 1].toKml();
                console.log("Repeated point! Type:" + type + " Polygon:" + name + " Pt:\n" + duplicate + duplicate);
                if (document.getElementById('outputErrors') != null  && document.getElementById('outputErrors').checked) {
                    correctedString = correctedString.replace(duplicate + duplicate, duplicate);
                    errorCount++;
                }
                coordsArray.pop();
            }
        }
    }
    coordsArray.type = type;
    coordsArray.name = name;
    coordsArray.filename = filename;
    // remove last item if polygon and duplicate
    if (type === "Polygon") {
        if (coordsArray.length > 1 && coordsArray[0].equals(coordsArray[coordsArray.length - 1]))
            coordsArray.pop();
        else {
            console.log("No duplicate end point! Type:" + type + " Polygon:\n" + name + "\n" + coordsArray[0].lng + "," + coordsArray[0].lat + "\n" + coordsArray[coordsArray.length - 1].lng + "," + coordsArray[coordsArray.length - 1].lat)
            errorCount++;
        }
    }
    // console.log("Found " + type + " " + coordsArray.length + " points");
    return coordsArray;
}

function coordsArraysToKml(coordsArrays) {
    let features = [];
    for (let i = 0; i < coordsArrays.length; i += 1)
        features.push(new Placemark(coordsArrays[i].type,coordsArrays[i].name,coordsArrays[i].styleUrl,coordsArrays[i]).setAltitudeMode(coordsArrays[i].altitudeMode));
    return features;
}

function colorHTMLToKML(htmlColor) {
    // No alpha
    return "ff" + htmlColor.substr(5, 2) + htmlColor.substr(3, 2) + htmlColor.substr(1, 2)
}

//returns an array of two polygons both include the shared points
function splitPolygon(polygon, index1, index2) {
    if (index1 > index2) {
        let temp = index1;
        index1 = index2;
        index2 = temp;
    }
    let segments = [];
    segments.push(polygon.slice(index1, index2 + 1));
    segments.push(polygon.slice(index2).concat(polygon.slice(0, index1 + 1)));
    return segments;
}

// function doSegmentsMatch(s1, s2, sensitivity) {
//     if (s1.length > 0 && s2.length > 0)
//         return s1[0].near(s2[s2.length - 1], sensitivity) && s1[s1.length - 1].near(s2[0], sensitivity);
//     return true;
// }

// function joinSegments(s1, s2, sensitivity) {
//     if (s1.length === 0 || s2.length === 0) {
//         console.log("Zero length segments!");
//         return false;
//     }
//     if (s1[s1.length - 1].near(s2[0], sensitivity))
//         return concatSegments(s1, s2);
//     else if (s2[s2.length - 1].near(s1[0], sensitivity))
//         return concatSegments(s2, s1);
//     else {
//       s2 = s2.slice(0);
//         s2.reverse();
//         if (s1[s1.length - 1].near(s2[0], sensitivity))
//             return concatSegments(s1, s2);
//         else if (s2[s2.length - 1].near(s1[0], sensitivity))
//             return concatSegments(s2, s1);
//         else {
//             console.log("Failed to match segments!");
//             return false;
//         }
//     }
// }
//Allow zero length segments
function joinSegmentsExact(s1, s2) {
    if (s1.length === 0)
        return s2;
    if (s2.length === 0)
        return s1;
    if (s1[s1.length - 1].equals(s2[0]))
        return concatSegments(s1, s2);
    else if (s2[s2.length - 1].equals(s1[0]))
        return concatSegments(s2, s1);
    else {
        s2 = s2.slice(0);
        s2.reverse();
        if (s1[s1.length - 1].equals(s2[0]))
            return concatSegments(s1, s2);
        else if (s2[s2.length - 1].equals(s1[0]))
            return concatSegments(s2, s1);
        else {
            //             console.log(s1, s2)
            return false;
        }
    }
}

function joinMultiSegmentsExact() {
    let args = (arguments.length === 1 ? [arguments[0]] : Array.apply(null , arguments));
    let result = args[0].slice(0);
    args.splice(0, 1);
    while (args.length > 0) {
        let match = args.findIndex(arg=>arg[0].equals(result[0])||arg[arg.length-1].equals(result[0])||arg[0].equals(result[result.length-1])||arg[arg.length-1].equals(result[result.length-1]));
        if (match === -1) {
            console.log("Segments don't match");
            return;
        }
        result = joinSegmentsExact(result, args[match]);
        args.splice(match, 1);
    }
    return result;
}

//concat segments removing duplicate points
function concatSegments(s1, s2) {
    let s = s1.concat(s2.slice(1));
    if (s[0].equals(s[s.length - 1]))
        s.pop();
    return s;
}

// what is one degree longitude in metres?
// assume sphere
function latToM() {
    let R = 6378137;
    let circumference = 2 * Math.PI * R;
    return circumference / 360;
}
// what is one degree latitude in metres at given latitude?
// assume sphere
function lngToM(lat) {
    let R = 6378137;
    return 2 * Math.PI * Math.sin(rad(90 - lat)) * R / 360;
}
function mToLat(m) {
    let R = 6378137;
    return m * 360 / (2 * Math.PI * R)
}
function mToLng(m, lat) {
    let R = 6378137;
    return m * 360 / (2 * Math.PI * Math.cos(lat.toRadians()) * R);
}
/** Extend Number object with method to pad with zeros */
if (Number.prototype.pad === undefined) {
    Number.prototype.pad = function(width) {
        let n = this + '';
        return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
    }
    ;
}

if (String.prototype.pad === undefined) {
    String.prototype.pad = function(width) {
        let n = this + '';
        return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
    }
}

function loadKml(fileControl) {
    let promise = new Promise(
    function(resolve, reject) {
        // Check for the various File API support.
        if (window.File && window.FileReader && window.FileList && window.Blob) {
        // Great success! All the File APIs are supported.
        } else
            alert('The File APIs are not fully supported in this browser.');
        let files = fileControl.files;
        if (files.length === 0) {
            alert("Please select a file");
            return;
        }
        let kmlStrings = [];
        //         kmlTexts.filenames = "";
        // Loop through the FileList and render image files as thumbnails.
        for (let i = 0, j = 0, f; f = files[i]; i += 1) {
            let reader = new FileReader();
            // Closure to capture the file information.
            reader.onload = (function(theFile) {
                return function(e) {
                    //                     kmlTexts.filenames += theFile.name.slice(0, -4) + " ";
                    if (theFile.name.slice(-4) === ".kml")
                        kmlStrings.push({
                            kmlString: e.target.result,
                            filename: theFile.name
                        });
                    else if (theFile.name.slice(-4) === ".kmz") {
                        let zip = new JSZip(e.target.result);
                        // for(let entryName in zip.files)
                        jQuery.each(zip.files, function(index, zipEntry) {
                            if (zipEntry.name.slice(-4) === ".kml")
                                kmlStrings.push({
                                    kmlString: zipEntry.asText(),
                                    filename: zipEntry.name
                                });
                            else
                                console.log("Non-KML file found in KMZ:" + zipEntry.name);
                        });
                    }
                    j++;
                    if (j === files.length)
                        resolve(kmlStrings);
                }
            })(f);
            if (f.name.slice(-4) === ".kml")
                reader.readAsText(f, "UTF-8");
            else if (f.name.slice(-4) === ".kmz")
                reader.readAsArrayBuffer(f);
            else
                alert("Unknown file type:" + f.name);
        }
    }
    );
    return promise;
}
function parseKmls(kmlStrings) {
    let kmls = [];
    kmlStrings.forEach(function(element, index, array) {
        kmls.push(parseKml(element.kmlString, element.filename));
    }
    );
    return kmls;
}
function parseKml(kmlString, filename) {
    let xmlDoc = jQuery.parseXML(kmlString);
    let $xml = jQuery(jQuery(xmlDoc).children()[0]);
    //     console.log($xml);
    let rootKml = new Kml();
    let getAttribute = function(attributes, attributeName) {
        if (typeof attributes !== 'undefined') {
            for (let i = 0; i < attributes.length; i += 1) {
                if (attributes[i].name === attributeName) {
                    return attributes[i].nodeValue;
                }
            }
        }
    }
    let attachAttributes = function(obj, attributes) {
        if (typeof attributes !== 'undefined') {
            for (let i = 0; i < attributes.length; i += 1) {
                obj[attributes[i].name] = attributes[i].nodeValue;
            }
        }
    }
    let processChildren = function(node, obj, attributes) {
        attachAttributes(obj, attributes);
        return node.children().each(function() {
            processXml(this, obj);
        }
        );
    }
    let processXml = function(xml, root) {
        let node = jQuery(xml);
        let nodeItem = node[0];
        //         console.log(node);
        let attributes = nodeItem.attributes;
        let nodeName = nodeItem.nodeName;
        let nodeContent = nodeItem.textContent.trim().split('&').join('&amp;');
        let simpleFields = ['name', 'styleUrl', 'open', 'heading', 'tilt', 'range', 'altitudeMode', 'gx:flyToMode', 'begin', 'end', 'text', 'longitude', 'latitude', 'altitude', 'gx:duration', 'scale',
        'color', 'width', 'key', 'href', 'tessellate', 'visibility', 'description', 'address', 'phoneNumber', 'north', 'south', 'east', 'west', 'minAltitude', 'maxAltitude', 'displayName',
        'value', 'refreshVisibility', 'flyToView', 'refreshMode', 'refreshInterval', 'viewRefreshMode', 'viewRefreshTime', 'viewBoundScale', 'viewFormat', 'httpQuery', 'roll', 'minLodPixels',
        'maxLodPixels', 'minRefreshPeriod', 'maxSessionLength', 'cookie', 'message', 'linkName', 'linkDescription', 'expires', 'targetHref', 'extrude', 'x', 'y', 'w', 'h', 'z',
        'drawOrder', 'rotation', 'gx:drawOrder', 'gx:x', 'gx:y', 'gx:w', 'gx:h', 'fill', 'listItemType', 'sourceHref', 'gx:altitudeOffset', 'outline', 'bgColor', 'textColor', 'displayMode', 'state',
        'gx:outerColor', 'gx:outerWidth', 'gx:physicalWidth', 'gx:labelVisibility', 'colorMode', 'shape', 'leftFov', 'rightFov', 'bottomFov', 'topFov', 'tileSize', 'maxWidth', 'maxHeight', 'gridOrigin', 'gx:delayedStart',
        'gx:playMode', 'minFadeExtent', 'maxFadeExtent', 'gx:interpolate'];
        if (simpleFields.indexOf(nodeName) !== -1) {
            if (nodeName.indexOf("gx:") === 0)
                root[nodeName.substring(3)] = nodeContent;
            else
                root[nodeName] = nodeContent;
            return;
        }
        let complexFieldsArrays = {
            'Document': {
                clss: Document,
                prop: 'features'
            },
            'Folder': {
                clss: Folder,
                prop: 'features'
            },
            'NetworkLink': {
                clss: NetworkLink,
                prop: 'features'
            },
            'Style': {
                clss: Style,
                prop: 'styles'
            },
            'StyleMap': {
                clss: StyleMap,
                prop: 'styles'
            },
            'Schema': {
                clss: Schema,
                prop: 'schemas'
            },
            'Pair': {
                clss: Pair,
                prop: 'pairs'
            },
            'Data': {
                clss: Data,
                prop: 'datas'
            },
            'Placemark': {
                clss: Placemark,
                prop: 'features'
            },
            'gx:Tour': {
                clss: Tour,
                prop: 'features'
            },
            'gx:FlyTo': {
                clss: FlyTo,
                prop: 'tourPrimitives'
            },
            'SimpleField': {
                clss: SimpleField,
                prop: 'simpleFields'
            },
            'gx:Wait': {
                clss: Wait,
                prop: 'tourPrimitives'
            },
            'gx:SoundCue': {
                clss: SoundCue,
                prop: 'tourPrimitives'
            },
            'gx:AnimatedUpdate': {
                clss: AnimatedUpdate,
                prop: 'tourPrimitives'
            },
            'gx:TourControl': {
                clss: TourControl,
                prop: 'tourPrimitives'
            },
            'GroundOverlay': {
                clss: GroundOverlay,
                prop: 'features'
            },
            'ScreenOverlay': {
                clss: ScreenOverlay,
                prop: 'features'
            },
            'PhotoOverlay': {
                clss: PhotoOverlay,
                prop: 'features'
            },
            'Alias': {
                clss: Alias,
                prop: 'aliass'
            },
            'ItemIcon': {
                clss: ItemIcon,
                prop: 'itemIcons'
            },
            'innerBoundaryIs': {
                clss: InnerBoundaryIs,
                prop: 'innerBoundaryIss'
            },


            'gx:SimpleArrayData': {
                clss: SimpleArrayData,
                prop: 'simpleArrayDatas'
            },

        }
        let complexFieldsProps = {
            'Link': {
                clss: Link,
                prop: 'link'
            },
            'gx:ViewerOptions': {
                clss: ViewerOptions,
                prop: 'viewerOptions'
            },
            'BalloonStyle': {
                clss: BalloonStyle,
                prop: 'balloonStyle'
            },
            'IconStyle': {
                clss: IconStyle,
                prop: 'iconStyle'
            },
            'LineStyle': {
                clss: LineStyle,
                prop: 'lineStyle'
            },
            'PolyStyle': {
                clss: PolyStyle,
                prop: 'polyStyle'
            },
            'ListStyle': {
                clss: ListStyle,
                prop: 'listStyle'
            },
            'LabelStyle': {
                clss: LabelStyle,
                prop: 'labelStyle'
            },
            'LookAt': {
                clss: LookAt,
                prop: 'abstractView'
            },
            'gx:Playlist': {
                clss: Playlist,
                prop: 'playlist'
            },
            'Icon': {
                clss: Icon,
                prop: 'icon'
            },
            'gx:TimeStamp': {
                clss: TimePrimitive,
                prop: 'timePrimitive'
            },
            'gx:TimeSpan': {
                clss: TimePrimitive,
                prop: 'timePrimitive'
            },
            'Region': {
                clss: Region,
                prop: 'region'
            },
            'Location': {
                clss: Location,
                prop: 'location'
            },
            'Orientation': {
                clss: Orientation,
                prop: 'orientation'
            },
            'Scale': {
                clss: Scale,
                prop: 'scale'
            },
            'ResourceMap': {
                clss: ResourceMap,
                prop: 'resourceMap'
            },

            'LatLonAltBox': {
                clss: LatLonAltBox,
                prop: 'latLonAltBox'
            },
            'Lod': {
                clss: Lod,
                prop: 'lod'
            },
            'LatLonBox': {
                clss: LatLonBox,
                prop: 'latLonBox'
            },
            'gx:LatLonQuad': {
                clss: LatLonQuad,
                prop: 'latLonQuad'
            },
            'ExtendedData': {
                clss: ExtendedData,
                prop: 'extendedData'
            },
            'Camera': {
                clss: Camera,
                prop: 'abstractView'
            },
            'NetworkLinkControl': {
                clss: NetworkLinkControl,
                prop: 'networkLinkControl'
            },
            'Update': {
                clss: Update,
                prop: 'update'
            },
            'Change': {
                clss: Change,
                prop: 'change'
            },
            'Create': {
                clss: Create,
                prop: 'create'
            },
            'Delete': {
                clss: Delete,
                prop: 'delete'
            },


            'SchemaData': {
                clss: SchemaData,
                prop: 'schemaData'
            },
            'outerBoundaryIs': {
                clss: OuterBoundaryIs,
                prop: 'outerBoundaryIs'
            },
            'ViewVolume': {
                clss: ViewVolume,
                prop: 'viewVolume'
            },
            'ImagePyramid': {
                clss: ImagePyramid,
                prop: 'imagePyramid'
            },

        }
        let vec2Fields = ['overlayXY', 'screenXY', 'rotationXY', 'size', 'hotSpot']
        let obj;
        if (complexFieldsArrays.hasOwnProperty(nodeName)) {
            obj = new complexFieldsArrays[nodeName].clss();
        } else if (complexFieldsProps.hasOwnProperty(nodeName)) {
            obj = new complexFieldsProps[nodeName].clss();
        } else if (vec2Fields.indexOf(nodeName) !== -1) {
            obj = new Vec2();
        }

        if (root instanceof Change) {
            if (typeof obj === 'undefined') {
                console.log(`Error: property not found: ${nodeName}`)
                return;
            }
            root.changes.push(obj);
            return processChildren(node, obj, attributes);
        }
        if (root instanceof Create) {
            if (typeof obj === 'undefined') {
                console.log(`Error: property not found: ${nodeName}`)
                return;
            }
            root.creates.push(obj);
            return processChildren(node, obj, attributes);
        }
        if (root instanceof Delete) {
            if (typeof obj === 'undefined') {
                console.log(`Error: property not found: ${nodeName}`)
                return;
            }
            root.deletes.push(obj);
            return processChildren(node, obj, attributes);
        }
        //         console.log(nodeName)

        if (complexFieldsArrays.hasOwnProperty(nodeName)) {
            if (typeof root[complexFieldsArrays[nodeName].prop] === 'undefined')
                console.log(`Error: property not found: ${complexFieldsArrays[nodeName].prop}`)
            root[complexFieldsArrays[nodeName].prop].push(obj);
            return processChildren(node, obj, attributes);
        }
        if (complexFieldsProps.hasOwnProperty(nodeName)) {
            root[complexFieldsProps[nodeName].prop] = obj;
            return processChildren(node, obj, attributes);
        }
        if (vec2Fields.indexOf(nodeName) !== -1) {
            attachAttributes(obj, attributes);
            root[nodeName] = obj;
            return;
        }
        function geometry(obj) {
            if (root instanceof MultiGeometry)
                root.geometries.push(obj);
            else
                root.geometry = obj;
            return processChildren(node, obj, attributes);
        }
        switch (nodeName) {
        case 'gx:value':
            root.contents.push(nodeContent);
            return;
        case 'gx:option':
            obj = {};
            root.options.push(obj);
            attachAttributes(obj, attributes);
            return;
        case 'SimpleData':
            obj = new SimpleData();
            attachAttributes(obj, attributes);
            obj.contents = nodeContent;
            root.simpleDatas.push(obj);
            return;


        case 'gx:altitudeMode':
            root.altitudeMode = nodeContent;
            return '';
        case 'MultiGeometry':
            return geometry(new MultiGeometry());
        case 'LineString':
            return geometry(new LineString());
        case 'Polygon':
            return geometry(new Polygon());
        case 'MultiTrack':
            return geometry(new MultiTrack());
        case 'Model':
            obj = new Model();
            if (root instanceof MultiGeometry)
                root.geometries.push(obj);
            if (root instanceof Track) {
                root.model = obj;
            }
            else {
                root.geometry = obj;
            }
            return processChildren(node, obj, attributes);

        case 'Track':
            obj = new Track();
            if (root instanceof MultiGeometry) {
                root.geometries.push(obj);
            }
            if (root instanceof MultiTrack) {
                root.tracks.push(obj);
            }
            else {
                root.geometry = obj;
            }
            return processChildren(node, obj, attributes);
        case 'Point':
            obj = new Point();
            if (root instanceof MultiGeometry)
                root.geometries.push(obj);
            else if (root instanceof PhotoOverlay) {
                root.point = obj;
            } else {
                root.geometry = obj;
            }
            return processChildren(node, obj, attributes);
        case 'LinearRing':
            obj = new LinearRing();
            if (root instanceof MultiGeometry) {
                root.geometries.push(obj);
            }
            else if (root instanceof Placemark) {
                root.geometry = obj;
            }
            else if (root instanceof OuterBoundaryIs) {
                root.linearRing = obj;
            }
            else if (root instanceof InnerBoundaryIs) {
                root.linearRings.push(obj);
            }
            return processChildren(node, obj, attributes);
        case 'linkSnippet':
            root.linkSnippet = nodeContent;
            root.linkSnippetMaxLines = getAttribute(attributes, "maxLines")
            return;
        case 'coordinates':
            root.coordinates = coordsStringToArray(nodeContent);
            return;
        case 'atom:author':
            root.author = nodeContent;
            return;
        case 'atom:link':
            root.linkHref = getAttribute(attributes, "href")
            return;
        case 'xal:AddressDetails':
            root.addressDetails = nodeContent;
            return;
        case 'Snippet':
            root.snippet = nodeContent;
            root.snippetMaxLines = getAttribute(attributes, "maxLines")
            return;
        case 'when':
            if (root instanceof Track)
                root.whens.push(nodeContent);
            else
                root.when = nodeContent;
            return;
        case 'gx:coord':
            let coords = nodeContent.split(' ');
            root.coords.push(new Coordinate(coords[1],coords[0],coords[2]));
            return;
        case 'gx:angles':
            let angle = nodeContent.split(' ');
            root.angles.push({
                heading: angle[0],
                tilt: angle[1],
                roll: angle[2]
            });
            return;
        default:
            console.log("Unknown tag: " + nodeItem.nodeName)
        }
    }
    processChildren($xml, rootKml);
    return rootKml;
}

function find(root, obj) {
    let objs = [];
    let findChildren = function(root) {
        if (root instanceof obj) {
            objs.push(root);
        }
        for (let propt in root) {
            let property = root[propt];
            if (typeof property === 'object') {
                if (Array.isArray(property)) {
                    for (let i = 0; i < property.length; i++)
                        findChildren(property[i]);
                } else {
                    findChildren(property);
                }
            }
        }
    }
    findChildren(root);
    return objs;
}