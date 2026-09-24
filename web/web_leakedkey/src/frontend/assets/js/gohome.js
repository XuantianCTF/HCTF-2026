
//获取cookie
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) { return c.substring(name.length, c.length); }
    }
    return "";
}
//为符合网关的定制的cas请求
function getService(service) {
    let loginservice = service;
    if (service && service.indexOf('shiro-cas?loginService') > 0) {
        loginservice = service.substring(0, service.indexOf("?"));
    }
    return loginservice;
}
//为符合网关的定制的cas请求1
function getService1(service, res) {
    //  
    //先解码
    let loginservice = decodeURIComponent(service);
    // loginservice=loginservice.replace('#', '%23').replace(/\&/g,"%26")
    if (service && service.indexOf('shiro-cas?loginService') > 0) {
        loginservice = service.substring(0, service.indexOf("?"));
    }
    //如果已有参数则拼接&
    if (loginservice.indexOf('?') > 0 || loginservice.indexOf('&') > 0) {
        loginservice += '&';
    } else {
        loginservice += '?';
    }
    let str = loginservice + "ticket=" + res;
    if (service.indexOf('shiro-cas?loginService') > 0) {
        let loginservice2 = service.substring(service.indexOf("loginService=") + 13);
        str += "&service=" + loginservice2
    }
    return str;
}
function receiveLoginData(resolve) {
    let service
    let xhr = new XMLHttpRequest()
    xhr.open('GET', (window.locale ? window.locale.casName : '/lyuapServer') + '/loginType/', false)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    xhr.send()
    if (xhr.readyState == 4) {
        service = JSON.parse(xhr.responseText).data.defaultLoginUrl
        console.log(service)
        resolve()
        return service
    } else {
        console.log(xhr)
    }
    xhr.onreadystatechange = function () {
    }

}
// 获取url参数
function getHashParam(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)'),
        queryString = window.location.search.split('?')[1] || '',
        result = queryString.match(reg)
    return result ? decodeURIComponent(result[2]) : null
}

function goHome() {
    //判断是否OAuth2.0
    let isOAuth2 = false
    if (window.location.pathname.indexOf('oauth2login') > -1
    ) {
        isOAuth2 = true
        let response_type =  getHashParam('response_type') || localStorage.getItem('response_type')
        let client_id = getHashParam('client_id') || localStorage.getItem('client_id')
        let redirect_uri = encodeURIComponent(getHashParam('redirect_uri')) || localStorage.getItem('redirect_uri')
        let scope = getHashParam('scope') || localStorage.getItem('scope')
        let state = getHashParam('state') || localStorage.getItem('state')
        localStorage.setItem('response_type', response_type)
        localStorage.setItem('client_id', client_id)
        localStorage.setItem('redirect_uri', redirect_uri)
        localStorage.setItem('scope', scope)
        localStorage.setItem('state', state)
    }
    let casName = '/lyuapServer';
    if (window.locale && window.locale.casName) {
        casName = window.locale.casName;
    }
    if (window.location.pathname.indexOf('logout') > 0) return
    if (window.location.pathname.indexOf('wx/loading') > 0) return
    if (window.location.pathname.indexOf('loginAgain') > 0) return
    //若cookie里面存在TGC，则使用其登录
    if (getCookie("CASTGC") || getCookie('session')) {
        //获取TGC
        let cookieTGC
        if (getCookie('CASTGC')) {//CASTGC优先判断
            cookieTGC = getCookie('CASTGC');

        } else if (localStorage.getItem('TGC')) {//兼容判断tgc
            cookieTGC = JSON.parse(localStorage.getItem('TGC')).tgt

        } else {//登录失败，回到登录页
            return
        }
        //获取去向地址
        let hash = window.location.search;
        hash = hash.substring(hash.indexOf("?") + 1);
        let serviceObject = hash;
        service = serviceObject.split('service=')[1];
        new Promise(function (resolve) {
            if (!service) {//没有跳转地址，则请求接口获取
                service = receiveLoginData(resolve)
            } else {
                resolve()
            }
        }).then(function () {
            //为符合网关的定制的cas请求1
            let loginService = getService(service);
            //登录
            let xhr = new XMLHttpRequest()
            if (isOAuth2) {
                let postUrl =
                    casName + '/oauth2/code/' + cookieTGC +
                    '?response_type=' + getHashParam('response_type') +
                    '&client_id=' + getHashParam('client_id') +
                    '&redirect_uri=' + encodeURIComponent(getHashParam('redirect_uri')) +
                    '&scope=' + getHashParam('scope') +
                    '&state=' + getHashParam('state')
                xhr.open('POST', postUrl, false)
            } else {
                xhr.open('POST', casName + '/v1/tickets/' + cookieTGC, false)
            }
            // 设置 Content-Type 为 application/x-www-form-urlencoded
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
            // 需要提交到服务端的数据可以通过 send 方法的参数传递
            // 格式：name=zhangsan&age=18
            xhr.send('service=' + loginService + '&loginToken=loginToken')
            let userData = {
            }
            let code, username
            if (xhr.readyState == 4 && xhr.status == 200) {
                let json
                try {
                    //返回对象
                    json = JSON.parse(xhr.responseText)
                } catch (e) {
                    console.log(e)
                    json = xhr.responseText
                }

                if (json) {
                    let codeStr = json;
                    if (json.meta) {
                        try {
                            code = json.data.code;
                            username = json.data.username;
                        } catch (e) {
                            if (codeStr.indexOf(';') !== -1) {
                                code = codeStr.split(';')[0];
                                username = codeStr.split(';')[1];
                            } else {
                                code = codeStr
                            }
                        }
                        if (code == "NOREGISTER") {
                            let unAuthorizeInfo = {
                                unAuthorizeUrl: service,
                                unAuthorizeType: '1'
                            }
                            sessionStorage.setItem("unAuthorizeInfo", JSON.stringify(unAuthorizeInfo));
                            // props.history.push("/loginUnAuthorize");
                            window.location.href = window.location.origin + "/loginUnAuthorize"
                            return;
                            //应用未授权
                        } else if (code == "NOAUTHORIZATION") {
                            let unAuthorizeInfo = {
                                unAuthorizeUrl: service,
                                unAuthorizeType: '2',
                                unAuthorizeName: username
                            };

                            sessionStorage.setItem("unAuthorizeInfo", JSON.stringify(unAuthorizeInfo));
                            // props.history.push("/loginUnAuthorize");
                            window.location.href = window.location.origin + "/loginUnAuthorize"
                            return;
                        } else if (code == "TWOVERIFY") {

                            console.log(window.location)
                            const content = codeStr.data;
                            userData.code = code;
                            userData.content = JSON.parse(content);
                            userData.userName = codeStr.username;
                            userData.vcodes = codeStr.uid;
                            userData.service = isOAuth2 ? getHashParam('redirect_uri') : service;
                            userData.type = "2";
                            userData.content = JSON.parse(content);
                            sessionStorage.setItem("twoverifyInfo", JSON.stringify(userData));
                            window.location.href = window.location.origin + '/loginAgain'
                            return;
                        }
                    }
                }
                //OAuth2.0跳转
                if (isOAuth2) {
                    let OAuth2_url = decodeURIComponent(json.data.redirectUri)
                    let signal = OAuth2_url.indexOf('?') > -1 ? '&' : '?'
                    let forwardUrl = OAuth2_url + signal + 'code=' + json.data.code + '&state=' + getHashParam('state')
                    window.location = forwardUrl
                    return
                }
                let gourl = getService1(service, xhr.responseText);
                window.location = gourl;
            } else {
                // alert('登录失败,请重新登录')
            }
            return
        })



    }




}

window.defaultLoginUrl = ''
goHome()

