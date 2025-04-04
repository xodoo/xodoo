import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { useInputField } from "../input_field_hook";
import { standardFieldProps } from "../standard_field_props";


import { Component,useState } from "@odoo/owl";

export class OpenUrlField extends Component {
    static template = "web.OpenUrlField";
    static props = {
        ...standardFieldProps,
        placeholder: { type: String, optional: true },
        text: { type: String, optional: true },
        websitePath: { type: Boolean, optional: true },
    };

    setup() {
        useInputField({ getValue: () => this.value });
        this.action = useService("action");
        this.state = useState(JSON.parse(this.env.model.config.activeFields[this.props.name].context.replace("'", '')))
    }

    get value() {
        return this.props.record.data[this.props.name] || "";
    }

    get formattedHref() {
        let value = this.props.record.data[this.props.name];
        debugger;
        if (value && !this.props.websitePath) {
            const regex = /^((ftp|http)s?:\/)?\//i; // http(s)://... ftp(s)://... /...
            value = !regex.test(value) ? `http://${value}` : value;
        }
        return value;
    }

    get isInEdition() {
        if (this.env.model.config.mode === "readonly") {
            return false;
        } else {
            return this.env.model.config.mode === "edit" || !this.env.model.config.resId;
        }
    }

    onClick() {
        if (this.isInEdition) {
            // 当前字段名称与值
            // const FieldName = this.props.name;
            // const FieldValue = this.props.record.data.name;
            // let jsonString = this.env.model.config.activeFields[FieldName].context.replace("'", '')
            // this.context = JSON.parse(jsonString);
            //"fun_type":"url", 上下文可以缺少
            var fu_type = this.state.fun_type;
            if (fu_type === undefined) {
                fu_type = 'url';
            }

            switch (fu_type) {
                case "url":
                    this._url();
                    break;
                case "ir.actions.client":
                    // this._ir_actions_client();
                    break;
                case "ir.actions.act_window":
                    // this._ir_actions_act_window()
                    console.log("I own a dog");
                    break;
                case "ir.actions.report":
                    // this._ir_actions_report();
                    break;
                case "ir.actions.server":
                    // this._ir_actions_server();
                    break;
                case "ir.actions.act_url":
                    // this._ir_actions_act_url();
                    break;
                case "from_qweb":
                    // this._from_qweb();
                    break;
                default:

                    break;
            }
        }
    }


    objectToUrlParams(obj) {
        let params = '';
        for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
                params += key + '=' + encodeURIComponent(obj[key]) + '&';
            }
        }
        return params.slice(0, -1);
    }

    _url() {
        let self = this;
        //窗口名称
        let tit = this.state.fun_windows_title;
        if (tit === undefined) (
            tit = '查询'
        )


        let fun_name = this.state.fun_name; //调用类型
        let url = this.state.form_url;

        let FieldName = this.props.name;
        let FieldValue = this.props.record.data.name;
        debugger
        let param = this.env.model.config.activeFields[FieldName].context.replace("'", '');

        //转成字符串放在url上做传值
        const urlParams = this.objectToUrlParams(this.state);

        //前台可以定义窗口大小
        let area = ['800px', '550px'];
        if (this.state.fun_area != undefined) {
            area = this.state.fun_area.split(',')
        }


        let index = layer.open({
            //标题
            title: tit,
            // 基本层类型：0（信息框，默认）1（页面层）2（iframe层，也就是解析content）3（加载层）4（tips层）
            type: 2,
            // 宽高：如果是100%就是满屏
            area: area,
            // 如果不想要界面滚动条可以这样写
            //content: ["内容/url",'no']
            content: url + "?" + urlParams,
            // 坐标：auto（默认坐标，即垂直水平居中），具体当文档：https://www.layui.com/doc/modules/layer.html#offset
            // offset: 'auto',
            // 遮罩透明度：默认：0.3透明度的黑色背景（'#000'）
            shade: 0.6,
            // 是否点击遮罩关闭：默认：false
            shadeClose: false,
            // 自动关闭所需毫秒：默认：0不会自动关闭
            time: 0,
            // 最大最小化：默认：false
            maxmin: true,
            anim: 0, // 0-6 的动画形式，-1 不开启
            // 固定：默认：true
            fixed: true,
            btnAlign: 'c',
            async: false,
            loading: true,
            params: this.state,
            // 是否允许拉伸：默认：true
            resize: true,
            // 层叠顺序：默认：19891014，一般用于解决和其它组件的层叠冲突
            zIndex: 19891014,
            // 关闭按钮：layer提供了两种风格的关闭按钮，可通过配置1和2来展示，如果不显示，则0
            closeBtn: 1,
            // 按钮：按钮1的回调是yes（也可以是btn1），而从按钮2开始，则回调为btn2: function(){}，以此类推
            btn: ['确定', '关闭'],
            // 第一个按钮事件，也可以叫btn1
            yes: function (index) {
                debugger
                //跳转不同的窗口
                switch (fun_name) {
                    case "url":
                        break;
                    case "map_point":
                        //百度点标注
                        self._url_map_point(this, index);
                        break;
                    case "from_qweb":
                        break;
                    default:
                        self._url_default(index);
                        break;
                }
                // 获取 iframe 的窗口对象
                // var iframeWin =  window[layero.find('iframe')[0]['name']];
                // var elemMark = iframeWin.$('#mark'); // 获得 iframe 中某个输入框元素
                // var value = elemMark.val();
                // if($.trim(value) === '') return elemMark.focus();
                // // 显示获得的值
                // layer.msg('获得 iframe 中的输入框标记值：'+ value);

                //最后关闭弹出层
                layer.close(index);
            }
            ,
            bt2: function (index, layer) {
                //点击第二个按钮执行
                // alert("点击第二个按钮执行")
            }
            ,

            // 右上角关闭按钮触发的回调：默认会自动触发关闭。如果不想关闭，return false即可
            cancel: function (index) {
                // if (layer.confirm('确定要关闭么')) { //只有当点击confirm框的确定时，该层才会关闭
                //     layer.close(index);
                // }
                layer.close(index);
                return false;
            }
            ,
            // 层销毁后触发的回调：无论是确认还是取消，只要层被销毁了，end都会执行，不携带任何参数。
            end: (index, layero) => {
                layer.close(index);
                // 层销毁后触发的回调：无论是确认还是取消，只要层被销毁了，end都会执行，不携带任何参数
                // alert("层销毁后触发的回调：无论是确认还是取消，只要层被销毁了，end都会执行，不携带任何参数")
            },
            // 层弹出后的成功回调方法：layero前层DOM，index当前层索引
            success:
                function (layero, index) {
                    // alert("巧妙的地方在这里哦")
                    var body = layer.getChildFrame('body', index);  //巧妙的地方在这里哦
                    //绑定查询条件
                    body.find('input[name = "search_name"]').val(FieldValue)
                    //传入界面上的参数到子页面
                    body.contents().find("#param").val(param);
                    // form.render(); //更新全部
                }

            // 最大化后触发的回调：携带一个参数，即当前层DOM
            ,
            full: function (layer) {
                // 最大化后触发的回调：携带一个参数，即当前层DOM
                // alert("最大化后触发的回调：携带一个参数，即当前层DOM");
            }
            ,
            // 最小化后触发的回调：携带一个参数，即当前层DOM
            min: function (layer) {
                // 最小化后触发的回调：携带一个参数，即当前层DOM
                //  alert("最小化后触发的回调：携带一个参数，即当前层DOM");
            }
            ,  // 还原后触发的回调：携带一个参数，即当前层DOM

            restore: function (layer) {
                // 还原后触发的回调：携带一个参数，即当前层DOM
                // alert("还原后触发的回调：携带一个参数，即当前层DOM");
            }
        });
    }

    //百度点标注
    _url_map_point(o, index) {
        debugger
        //当点击‘确定'按钮的时候，获取弹出层返回的值
        var res = window["layui-layer-iframe" + index].callbackdata();
        o.props.record.update({[o.props.fieldName]: res.point});

        return true;
    }

    //通用弹出窗口
    _url_default(index) {
        //当点击‘确定'按钮的时候，获取弹出层返回的值
        debugger;
        var iframeWindow = window['layui-layer-iframe' + index];
        //数据值
        var checkStatus = iframeWindow.layui.table.checkStatus('control_table');
        var data = checkStatus.data;
        if (data.length == 1) {
            let arr = this.state.fun_write_field.split(",");
            var dict = {}; // 可以绑定多个字段
            for (let i = 0; i < arr.length; i++) {
                let a = arr[i].split(":");
                if (a[1] != "") {
                    if (a[2] == "Many2one") {
                        dict[a[0]] = data[0][a[1]].split(",");
                    } else if (a[2] == "Many2many") {
                        // dict[a[0]] = [6, false, data[0][a[1]].split(",")] ;
                        // dict[a[0]] =[[6, 0,[1,2]]];
                        // dict[a[0]] =[[6, 0, [1,2]]];
                    } else {
                        dict[a[0]] = data[0][a[1]];
                    }
                }
            }
            debugger;
            if (arr.length == 0) {

                this.props.record.update({[this.props.name]: data[0].name});
            } else {
                this.props.record.update(dict);
            }

            // layer.msg(data[0].caseNature);
            // $("#caseNature").html(data[0].caseNature);
        } else {
            layer.msg("请选择一个值！");
        }
    }


    get _ir_actions_client() {
    }

    get _ir_actions_act_window() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "res.partner",
            res_id: 1,
            views: [[false, "form"]],
            target: "new",
        });
    }


    get _ir_actions_report() {
        // this.actionService.doAction({
        //     type: "ir.actions.report",
        //     report_type: "qweb-pdf",
        //     report_name: `event.event_registration_report_template_badge/${this.registration.id}`,
        // });
    }

    get _ir_actions_server() {
    }

    _ir_actions_act_url() {
        let url = "/amos/index";
        // this.action.doAction({type: "ir.actions.act_url", url});
        this.action.doAction({
            name: "JS Tests",
            target: "new",
            type: "ir.actions.act_url",
            url: url,
        });

    }




}

export const openUrlField = {
    component: OpenUrlField,
    displayName: _t("Open URL"),
    supportedOptions: [
        {
            label: _t("Is a website path"),
            name: "website_path",
            type: "boolean",
            help: _t("If True, the url will be used as it is, without any prefix added to it."),
        },
    ],
    supportedTypes: ["char"],
    extractProps: ({ attrs, options }) => ({
        text: attrs.text,
        websitePath: options.website_path,
        placeholder: attrs.placeholder,
    }),
};

registry.category("fields").add("open_url", openUrlField);

class FormOpenUrlField extends OpenUrlField {
    static template = "web.FormOpenUrlField";
}

export const formOpenUrlField = {
    ...openUrlField,
    component: FormOpenUrlField,
};

registry.category("fields").add("form.open_url", formOpenUrlField);
