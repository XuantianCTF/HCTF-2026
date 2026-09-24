/*
 * @Description: 语言配置
 */
window.locale = {
    casName: '/authServer',
    isRememberPass: '1',
    list: [
      {
        name: '中 文',
        type: 'zh_CN',
        //img: 'assets/images/language/zh_CN.png',
        tip: 'language_zh_CN'
      },
      {
        name: '英 文',
        type: 'en_US',
        //img: 'assets/images/language/en_US.png',
        tip: 'language_en_US'
      },
      {
        name: '藏 文',
        type: 'zh_TT',
        //img: 'assets/images/language/en_US.png',
        tip: 'language_zh_TT'
      }
    ],
    No_text: 'text-absent',
    zh_CN: {
      //首页
      account: '账号',
      name: '姓名',
      alias: '别名',
      ID_card: '身份证号',
      pass_login: '账户登录',
      sms_login: '手机登录',
      scan_login: '扫码登录',
      finger_login: '指纹登录',
      ukey_login: 'Ukey登录',
      login_wait: '登录中，请稍等..........',
      scan_login_easy: '扫码登录更方便',
      immediately_login: '即将登录：',
      enter_account: '请输入学号/工号',
      enter_pass: '请输入密码',
      enter_arithmetic_answer: '请输入算术答案',
      remember_pass_seven_days: '七天之内记住密码',
      remember_pass: '记住密码',
      common_problem: '常见问题',
      forget_pass: '忘记密码',
      account_appeal: '账号申诉',
      enter_name: '请输入您的姓名',
      enter_ID_card: '请输入您的身份证',
      query: '查询',
      close: '关闭',
      account_query: '账号查询',
      login: '登录',
      reset: '重置',
      verify_wait: '验证中，请稍等...',
      enter_phone: '请输入您的手机号',
      phone_format_error: '手机号格式不正确',
      enter_security_code: '请输入短信验证码',
      send_security_code: '发送验证码',
      security_code_invalid: '请点击重新获取',
      QQ_login: 'QQ登录',
      weibo_login: '微博登录',
      dingding_login: '钉钉登录',
	  Dd_scan_login: '钉钉扫码',
      first_install_ukey: '请先安装Ukey驱动！',
      back_account_login: '返回账号登录',
      QR_code_invalid: '二维码已失效',
      click_refresh: '请点击刷新',
      WeChat_scan_login: '微信扫码',
      APP_scan_login: 'APP扫码',
      auth_scan_login: '聚合认证扫码登录',
      account_login: '账户登录',
      Qr_code_Login: '二维码登录',
      login_failure: '登录失败',
      verification_code_error: '验证码错误',
      warn: '提示',
      send_sms_code_success: '发送短信验证码成功',
      ukey_insert: 'UKEY已被插入',
      ukey_pull: 'UKEY已被拨出',
      ukey_login_not_use: 'UEKY登录无法使用，请联系管理员！',
      query_fail: '查询失败',
      not_find_use: '没有找到相应的用户！请查找数据是否正确！',
      information_portal: '信息门户',
      browser_recommended: '推荐使用浏览器',
  
      //指纹登录
      finger_scan_login: '指纹扫描登录',
      finger_login_step1: '设备未连接',
      finger_login_step2: '请按手指',
      finger_login_step3: '请抬起手指',
      finger_login_step4: '采集图像成功',
      finger_login_step5: '采集指纹特征点完成',
      finger_login_step6: '登记指纹特征点完成',
      finger_match_fail: '指纹匹配失败,请重新匹配或采集指纹!',
      browser_not_ws: '浏览器不支持ws协议,请使用IE浏览器',
      connect_usb_fail: '连接USB指纹仪失败',
      open_usb_fail: '打开USB指纹仪失败',
      connect_finger_fail: '连接指纹仪超时',
      change_browser: '火狐浏览器不支持,请更换其它浏览器!',
      collect_finger_fail: '采集指纹特征点失败',
      register_finger_fail: '登记指纹特征点失败',
  
  
      //Ukey登录
      enter_pin_code: '请输入PIN码',
      ie_insert_ukey: 'IE浏览器下插入Ukey后需刷新页面',
      not_check_device: '未检测到设备',
  
      //页脚
      company: '',
      copyright_company: '版权所有©大学',
      login_pageInfo_4: '统一身份认证平台-认证中心',
  
      //页头
      person_center: '个人中心',
      setting: '设置',
      exit_login: '退出登录',
      change_theme: '切换主题',
  
      //再次登录
      tip_encrypted_phone: '温馨提示：密保验证或手机验证',
      security_setting: '安全设置',
      verify_way: '验证方式',
      select_verify_way: '请选择验证方式',
      phone_verify: '手机验证',
      encrypted_verify: '密保验证',
      security_code: '验证码',
      encrypted_question: '密保问题',
      select_encrypted_question: '请选择密保问题',
      question_answer: '问题答案',
      question_answer_not_empty: '问题答案不能为空',
      confirm: '确认',
      auth_fail: '验证失败',
      bind_phone: '请绑定手机号',
      bind_email: '请绑定邮箱',
      tip_romote_login: '异地登录提示：此登录IP为您不常用的登录IP地址，请验证您的密保或者手机',
      romote_login: '异地登录',
      flag_romote_login: '是否标记此登录IP为常用IP',
  
      //登录绑定QQ
      bind_QQ_tip1: '认证平台账号绑定 ：该QQ第一次登录使用，需要进行认证中心的账号密码校验，校验成功后即可绑定对应账号，下一次使用QQ登录时将直接进入认证中心。',
      bind_QQ_tip2: '认证中心账号',
      bind_QQ_tip3: '认证中心密码',
      save: '保存',
      QQ_bind: 'QQ绑定',
  
      //登录绑定微博
      bind_WeiBo_tip1: '认证平台账号绑定 ：该微博第一次登录使用，需要进行认证中心的账号密码校验，校验成功后即可绑定对应账号，下一次使用微博登录时将直接进入认证中心。',
      WeiBo_bind: '微博绑定',
  
      //登录绑定钉钉
      bind_DingDing_tip1: '认证平台账号绑定 ：该钉钉第一次登录使用，需要进行认证中心的账号密码校验，校验成功后即可绑定对应账号，下一次使用钉钉登录时将直接进入认证中心。',
      DingDing_bind: '钉钉绑定',
  
      //登录绑定微信
      bind_WeChat_tip1: '温馨提示：您可以通过企业微信或者微信扫码，来绑定当前登录认证的账号，绑定成功之后，您下次可通过微信或者企业微信扫码登录认证、扫码找回密码等功能。注意：请先关注企业微信后在扫码绑定',
      bind_WeChat_tip2: '微信/企业微信扫码绑定',
  
      //登录校验
      login_check_tip1: '密保设置 ：欢迎您，',
      login_check_tip2: '，请填写您的密保问题和答案，保存成功后，可以使用密保找回密码和登录验证等功能。',
      login_check_tip3: '手机验证绑定 ：欢迎您，',
      login_check_tip4: '，请填写您的手机号，点击发送验证码，系统会向您的手机发送短信，您需要输入短信内容中的验证码，来完成验证',
      login_check_tip5: '邮箱验证绑定 ：欢迎您，',
      login_check_tip6: '，请填写您的邮箱，点击发送验证码，系统会向您的邮箱发送邮件，您需要输入邮件内容中的验证码，来完成验证',
      first_teacher: '您的第一位老师叫什么',
      library_card_number: '您的图书卡号码是什么',
      common_QQ: '您常用的QQ号码是多少',
      first_phone: '您的第一个电话号码是多少',
      luck_number: '您的幸运数字是多少',
      custom_question: '自定义问题',
      custom_question_not_empty: '自定义问题不能为空',
      phone: '手机号',
      check: '校验',
      email: '邮箱',
      enter_email: '请输入邮箱',
      email_format_error: '邮箱格式不正确',
      send_email_code_success: '发送邮箱验证码成功',
      send_sms_code_fail: '发送短信验证码失败，请勿短时间内多次发送，2分钟后再尝试！',
      send_email_code_fail: '发送邮箱验证码失败',
      encrypted_bind: '密保绑定',
      encrypted_bind_fail: '密保绑定失败！',
      phone_bind: '手机号绑定',
      phone_bind_fail: '手机号绑定失败！',
      email_bind: '邮箱绑定',
      email_bind_fail: '邮箱绑定失败！',
  
      //登录错误
      login_error_tip1: '访问被拒绝！',
      login_error_tip2: '可能由于',
      login_error_tip3: '您无权访问该系统',
      login_error_tip4: '您访问的地址不对',
      login_error_tip5: '如有任何问题，请及时联系管理员处理',
      login_error_tip6: '您还可以',
      login_error_tip7: '重新登录或稍后再试。',
  
      //登录未授权
      login_unAuthorize_tip1: '应用未注册！',
      login_unAuthorize_tip2: '应用未授权！',
      login_unAuthorize_tip3: '该应用未在认证平台登记注册',
      login_unAuthorize_tip4: '你无权访问该应用',
      login_unAuthorize_tip5: '如有任何问题，请及时联系管理员处理',
      login_unAuthorize_tip6: '您还可以',
      login_unAuthorize_tip7: '重新',
      login_unAuthorize_tip8: '登录或稍后再试',
  
      //第一次登录
      first_login_tip1: '温馨提示:此账号首次登录或者密码过期，必须重新设置密码，新密码不能与初始密码相同,',
      first_login_tip2: '且密码由',
      first_login_tip3: '个字符组成，区分大小写（至少含数字',
      first_login_tip4: '位、含字母',
      first_login_tipUpper: '位、含大写字母',
      first_login_tipLower: '位、含小写字母',
      first_login_tip5: '位、含特殊字符',
      first_login_tip6: '位，不能包含空格）建议使用英文字母加数字或符号的混合密码',
      new_pass: '新密码',
      enter_new_pass: '请输入新密码',
      pass_class: {
        strong: '强',
        middle: '中',
        weak: '弱'
      },
      confirm_pass: '确认密码',
      enter_confirm_pass: '请输入确认密码',
      change_password: '修改密码',
      change_password_fail: '修改密码失败！',
      the_two_passwords_are_not_the_same: '两次输入的密码不一致!',
      password_length_error1: '密码长度错误,密码长度应在',
      password_length_error2: '和',
      password_length_error3: '之间！',
      password_error_digits1: '密码应至少包含',
      password_error_digits2: '位数字!',
      password_error_letters1: '密码应至少包含',
      password_error_letters2: '位字母!',
      password_error_specialchar1: '密码应至少包含',
      password_error_specialchar2: '位特殊字符!',
      password_without_whitespace: '密码不能包含空格',
  
      //登录提交
      reject: '拒绝',
      warm_prompt: '温馨提示',
  
      //注销
      logout_fail: '注销失败',
      logout_ticket_fail: '注销票据失败',
  
      //微信扫码
      loading_wait: '正在加载中，请稍后...',
      Qr_code_invalid_scan: '此二维码已过期，请重新扫描',
      WeChat_scan_tip1: '您尚未关注微信企业号，请长按上图二维码进行关注',
      WeChat_scan_tip2: '您尚未关注微信公众号，请长按上图二维码进行关注',
      binding_success: '绑定成功',
      login_success: '登录成功',
      login_name_not_empty: '登录名不能为空',
      pass_not_empty: '密码不能为空',
      account_pass: '账号密码',
      phone_code: '手机验证码',
      confirm_login: '确认登录',
      cancel_login: '取消登录',
      binding_account_yet: '检测到您已经绑定过账号',
      WeChat_scan_tip2: '首次登录请输入认证平台的账号和密码进行绑定',
      is_binding_account: '是否绑定账号',
      confirm_binding: '确认绑定',
      cancel_binding: '取消绑定',
      WeChat_scan_tip3: '检测到账号已被绑定，请更换其他微信号进行绑定',
      WeChat_bind: '微信绑定',
      self_bind_tip: '操作失败，请手动绑定',
      confirm_unbinding: '确认解绑',
      cancel_unbinding: '取消解绑',
      //同一人多账号
      user_account_select: '用户类型账号选择',
      user_account_select_one: '请选择一个用户类型账号为默认登录账号',
      user_account_select_tip_1: '温馨提示:请选择登录用户类型账号，所选用户类型账号将会被用作',
      user_account_select_tip_2: '默认登录账号',
      user_account_select_tip_3: '，下次登录会直接登录默认账号！',
      user_account_select_tip_4: '若找不到用户类型账号，可尝试',
      user_account_select_tip_5: '左右滑动',
      user_account_select_tip_6: '查找更多用户类型账号',
      user_account_select_tip_7: '账号：',
      user_account_select_tip_8: '身份：',
      //登录参数
      code_false: '验证码错误',
      nouser: '用户名或密码错误。',
      user_disabled: '账号被停用，请联系相关管理员处理。',
    },
    en_US: {
      //首页
      account: 'Account',
      name: 'Name',
      alias: 'Alias',
      ID_card: 'ID card',
      pass_login: 'Password login',
      sms_login: 'SMS login',
      scan_login: 'Scan login',
      finger_login: 'Finger login',
      ukey_login: 'Ukey login',
      login_wait: 'Please wait while logging in..........',
      scan_login_easy: 'Scan code login more convenient',
      immediately_login: 'The login：',
      enter_account: 'Please enter account number',
      enter_pass: 'Please enter password',
      enter_arithmetic_answer: 'Please enter arithmetic answer',
      remember_pass_seven_days: 'Remember password within seven days',
      remember_pass: 'Keep password',
      common_problem: 'Problem',
      forget_pass: 'Find password',
      account_appeal: 'Appeal account',
      enter_name: 'Please enter name',
      enter_ID_card: 'Please enter ID card',
      query: 'Query',
      close: 'Close',
      account_query: 'Query account',
      login: 'Login',
      reset: 'Reset',
      verify_wait: 'Please wait while verifying...',
      enter_phone: 'Please enter phone number',
      phone_format_error: 'Incorrect phone number format',
      enter_security_code: 'Please enter security code',
      send_security_code: 'Please send security code',
      QQ_login: 'QQ login',
      weibo_login: 'WeiBo login',
      dingding_login: 'DingDing login',
      first_install_ukey: 'Please install the Ukey driver first!',
      back_account_login: 'Return to account login',
      QR_code_invalid: 'Qr code is invalid',
      click_refresh: 'Click refresh',
      WeChat_scan_login: 'WeChat scan',
      APP_scan_login: 'APP scan',
      auth_scan_login: 'Authentication scan',
      account_login: 'Account login',
      Qr_code_Login: 'Qrcode login',
      login_failure: 'Login failure',
      verification_code_error: 'Verification code error',
      warn: 'Warn',
      send_sms_code_success: 'SMS verification code sent successfully',
      ukey_insert: 'The UKEY has been inserted',
      ukey_pull: 'The UKEY has been dialed',
      ukey_login_not_use: 'UEKY login cannot be used, please contact the administrator!',
      query_fail: 'The query fails',
      not_find_use: 'No corresponding user was found! Please check if the data is correct!',
      information_portal: 'Information portal',
      auth_fail: 'Authentication failed',
      bind_phone: 'Please bind the phone number',
      bind_email: 'Please bind email',
      browser_recommended: 'Browser Recommended',
      tip_romote_login: 'Note: This login IP address is not commonly used by you. Please verify your password or mobile phone',
      romote_login: 'Romote Login',
      flag_romote_login: 'Whether to mark the login IP address as a common IP address',
  
      //指纹登录
      finger_scan_login: 'Fingerprint scanning login',
      finger_login_step1: 'Device not connected',
      finger_login_step2: 'Please press your finge',
      finger_login_step3: 'Please raise your finger',
      finger_login_step4: 'Image acquisition successful',
      finger_login_step5: 'Fingerprint characteristic points are collected',
      finger_login_step6: 'Registration of fingerprint feature points is completed',
      finger_match_fail: 'Fingerprint match failed, please rematch or collect fingerprint!',
      browser_not_ws: 'Fingerprint match failed, please rematch or collect fingerprint!',
      connect_usb_fail: 'USB fingerprint reader failed to connect',
      open_usb_fail: 'USB fingerprint reader failed to open',
      connect_finger_fail: 'Connect the fingerprint reader timeout',
      change_browser: 'Firefox is not supported, please change to another browser!',
      collect_finger_fail: 'Failed to collect fingerprint feature points',
      register_finger_fail: 'Registration of fingerprint feature points failed',
  
      //Ukey登录
      enter_pin_code: 'Please enter the PIN code',
      ie_insert_ukey: 'Refresh the page after inserting Ukey in Internet Explorer',
      not_check_device: 'No device detected',
  
      //页脚
      company: 'Technology Co., LTD',
      copyright_company: 'Copyright ©  University. All Rights Reserved',
      login_pageInfo_4: 'Unified Identity authentication platform - Authentication center',
  
  
      //页头
      person_center: 'Personal Center',
      setting: 'Setting',
      exit_login: 'Exit Login',
      change_theme: 'Change Theme',
  
      //再次登录
      tip_encrypted_phone: 'Tips: secret protection verification or mobile phone verification',
      security_setting: 'Security Settings',
      verify_way: 'Verification mode',
      select_verify_way: 'Please select the method of validation',
      phone_verify: 'verification of mobile phone',
      encrypted_verify: 'Encrypted authentication',
      security_code: 'Security code',
      encrypted_question: 'Security question',
      select_encrypted_question: 'Please select secret protection problem',
      question_answer: 'The answer to the question',
      question_answer_not_empty: 'The answer to the question cannot be empty',
      confirm: 'Confirm',
  
      //登录绑定QQ
      bind_QQ_tip1: 'Authentication platform account binding: This QQ login for the first time needs to verify the account password of the authentication center. After successful verification, the corresponding account can be bound. The next time you use QQ login, you will directly enter the authentication center.',
      bind_QQ_tip2: 'Account of certification Center',
      bind_QQ_tip3: 'Authentication center password',
      save: 'Save',
      QQ_bind: 'QQ bind',
  
      //登录绑定微博
      bind_WeiBo_tip1: 'Account binding of authentication platform: For the first time to log in and use this Weibo, it is necessary to verify the account password of the Certification Center. After successful verification, the corresponding account can be bound. The next time to log in on Weibo, it will directly enter the Certification Center.',
      WeiBo_bind: 'Weibo Binding',
  
      //登录绑定钉钉
      bind_DingDing_tip1: 'Authentication platform account binding: for the first time, the account password of the authentication center needs to be verified. After the verification is successful, the corresponding account can be bound. The next time you log in with the key, you will directly enter the authentication center.',
      DingDing_bind: 'DingDing Binding',
  
      //登录绑定微信
      bind_WeChat_tip1: 'Warm tip: you can bind the current login authentication account by scanning WeChat or WeChat. After the binding is successful, you can login authentication and retrieve password by scanning WeChat or WeChat next time.Note: please pay attention to enterprise WeChat before scanning the code binding',
      bind_WeChat_tip2: 'WeChat/Enterprise WeChat scan code binding',
  
      //登录校验
      login_check_tip1: 'Encryption Settings: Welcome,',
      login_check_tip2: ', please fill in your secret protection question and answer, after saving successfully, you can use the secret protection to retrieve the password and login authentication and other functions.',
      login_check_tip3: 'Mobile authentication binding: Welcome,',
      login_check_tip4: ', please fill in your mobile phone number, click send verification code, the system will send a message to your mobile phone, you need to enter the verification code in the message content, to complete the verification',
      login_check_tip5: 'Mailbox verification binding: Welcome,',
      login_check_tip6: ', please fill in your mailbox and click send verification code. The system will send an email to your mailbox. You need to enter the verification code in the email to complete the verification',
      first_teacher: 'What was your first teacher\'s name',
      library_card_number: 'What\'s your library card number',
      common_QQ: 'What\'s your usual QQ number',
      first_phone: 'What\'s your first telephone number',
      luck_number: 'What\'s your lucky number',
      custom_question: 'Custom problem',
      custom_question_not_empty: 'The custom problem cannot be empty',
      phone: 'Phone',
      check: 'Check',
      email: 'Email',
      enter_email: 'Please enter email address',
      email_format_error: 'Incorrect email format',
      send_email_code_success: 'The email verification code was sent successfully',
      send_sms_code_fail: 'Failed to send SMS verification code,Please do not send it many times in a short time. Try again after 2 minutes!',
      send_email_code_fail: 'Failed to send email verification code',
      encrypted_bind: 'Encrypted binding',
      encrypted_bind_fail: 'Encrypted binding failed!',
      phone_bind: 'Phone binding',
      phone_bind_fail: 'Phone binding failed!',
      email_bind: 'Email binding',
      email_bind_fail: 'Email binding failed!',
  
      //登录错误
      login_error_tip1: 'Access denied!',
      login_error_tip2: 'May be due to',
      login_error_tip3: 'You do not have access to the system',
      login_error_tip4: 'The address you visited is wrong',
      login_error_tip5: 'If you have any questions, please contact the administrator in time',
      login_error_tip6: 'You can also',
      login_error_tip7: 'Log in again or try again later.',
  
      //登录未授权
      login_unAuthorize_tip1: 'Application not registered!',
      login_unAuthorize_tip2: 'Unauthorized application!',
      login_unAuthorize_tip3: 'The application is not registered on the authentication platform',
      login_unAuthorize_tip4: 'You don\'t have access to the app',
      login_unAuthorize_tip5: 'If you have any questions, please contact the administrator in time',
      login_unAuthorize_tip6: 'You can also',
      login_unAuthorize_tip7: '',
      login_unAuthorize_tip8: 'Log in again or try again later',
  
      //第一次登录
      first_login_tip1: 'Warm tip: If the account is logged in for the first time or the password has expired, you must reset the password. The new password cannot be the same as the original password.',
      first_login_tip2: 'The password is composed of ',
      first_login_tip3: ' characters, case sensitive (at least ',
      first_login_tip4: ' digits, ',
      first_login_tip5: ' digits, ',
      first_login_tip6: ' digits for special characters, no Spaces). It is recommended to use a mixed password of English letters and Numbers or symbols',
      new_pass: 'New password',
      enter_new_pass: 'Please enter new password',
      pass_class: {
        strong: 'Strong',
        middle: 'Middle',
        weak: 'Weak'
      },
      confirm_pass: 'Confirm password',
      enter_confirm_pass: 'Please enter confirmation password',
      change_password: 'Change password',
      change_password_fail: 'Password change failed!',
      the_two_passwords_are_not_the_same: 'The two passwords are not the same',
      password_length_error1: 'Password length error, the length should be between ',
      password_length_error2: ' and ',
      password_length_error3: ' !',
      password_error_digits1: 'The password contains at least ',
      password_error_digits2: ' digits!',
      password_error_letters1: 'The password contains at least ',
      password_error_letters2: ' letters!',
      password_error_specialchar1: 'The password contains at least ',
      password_error_specialchar2: ' special characters!',
      password_without_whitespace: 'The password cannot contain spaces',
  
      //登录提交
      reject: 'Reject',
      warm_prompt: 'Warm prompt',
  
      //注销
      logout_fail: 'Logout failed',
      logout_ticket_fail: 'Cancellation of note failure',
  
      //微信扫码
      loading_wait: 'Loading. Please wait...',
      Qr_code_invalid_scan: 'This QR code has expired, please scan it again',
      WeChat_scan_tip1: 'You have not followed the WeChat enterprise number, please long press the two-dimensional code above to follow',
      binding_success: 'Binding success',
      login_success: 'Login success',
      login_name_not_empty: 'The login name cannot be empty',
      pass_not_empty: 'The password cannot be empty',
      account_pass: 'Account password',
      phone_code: 'Phone security code',
      confirm_login: 'Confirm Login',
      cancel_login: 'Cancel Login',
      binding_account_yet: 'It has been detected that you have bound an account',
      WeChat_scan_tip2: 'For the first time login, please enter the account and password of the authentication platform for binding',
      is_binding_account: 'Whether to bind the account',
      confirm_binding: 'Confirm Binding',
      cancel_binding: 'Cancel Binding',
      WeChat_scan_tip3: 'It has been detected that the account has been bound, please replace it with another WeChat ID for binding',
      WeChat_bind: 'WeChat bind',
      self_bind_tip: 'If the user is invalid, contact the administrator',
      confirm_unbinding: 'Confirm Unbinding',
      cancel_unbinding: 'Cancel Unbinding',
      //同一人多账号
      user_account_select: 'User type account selection',
      user_account_select_one: 'Please select a user type account as the default login account',
      user_account_select_tip_1: 'Warm tip: Please select the login user type account, the selected user type account will be used as',
      user_account_select_tip_2: ' default login account',
      user_account_select_tip_3: ',Next time you log in, you\'ll log in to your default account!',
      user_account_select_tip_4: 'If you can\'t find a user type account, try it',
      user_account_select_tip_5: ' sliding around',
      user_account_select_tip_6: ' find more user type accounts',
      user_account_select_tip_7: 'Account：',
      user_account_select_tip_8: 'Identity：',
      //登录参数
      code_false: 'The verification code is incorrect',
      nouser: 'Account number does not exist.：',
      user_disabled: 'If the account is deactivated, please contact the relevant administrator to deal with it.',
    },
    zh_TT: {
  
      //首页
      account: 'རྩིས་ཐོའི་ཨང་གྲངས།',
      name: 'རུས་མིང་།',
      alias: 'མིང་གཞན།',
      ID_card: 'ཐོབ་ཐང་ལག་ཁྱེར་གྱི་ཨང་གྲངས།',
      pass_login: 'གསང་ཨང་ཐོ་འགོད།',
      sms_login: 'འཕྲིན་ཐུང་བཀོལ་ནས་ཐོ་འཇུག་།',
      scan_login: 'བཤེར་འབེབས་ཚད་གཉིས་ཨང་ཐོ་འཇུག',
      finger_login: 'མཛུབ་རིས་ཐོ་འཇུག་།',
      ukey_login: 'Ukeyཐོ་འཇུག་།',
      login_wait: 'སྐམ་སར་འཛེགས་ནས་ཁྲོད་།, ཅུང་ཙམ་འགོར་རྗེས་།..........',
      scan_login_easy: 'རྩ་གཉིས་ཨང་རྟགས་བཤར་འབེབས་ཐོ་འཇུག་དེ་བས་སྟབས་བདེ་།',
      immediately_login: 'ཐོ་འཇུག་བྱེད་ཉེ།：',
      enter_account: 'རོགས་།ཁྱེད་རང་གི་རྩིས་ཐོའི་ཨང་གྲངས་ནང་འཇུག་།',
      enter_pass: 'གསང་ཨང་ནང་འཇུག་རོགས་།',
      enter_arithmetic_answer: 'རོགས་།ཨང་རྩིས་ཀྱི་དྲིས་ལན་ནང་འཇུག་།',
      remember_pass_seven_days: 'ཉིན་བདུན་གྱི་ནང་དུ་གསང་གྲངས་ཡིད་ལ་བཟུང་།',
      remember_pass: 'གསང་གྲངས་ཡིད་ལ་བཟུང་།',
      common_problem: 'རྒྱུན་མཐོང་གི་གནད་དོན་།',
      forget_pass: 'གསང་གྲངས་བརྗེད་སོང་།',
      account_appeal: 'རྩིས་ཐོའི་ཨང་གྲངས་རྒྱུ་མཚན་ཞུ་འབུལ།',
      enter_name: 'རོགས་།ཁྱེད་རང་གི་རུས་མིང་ནང་འཇུག་།',
      enter_ID_card: 'རོགས་།ཁྱེད་རང་གི་ཐོབ་ཐང་ལག་ཁྱེར་ནང་འཇུག་།',
      query: 'འདྲི་རྩད་།',
      close: 'སྒོ་རྒྱག་རོགས།',
      account_query: 'རྩིས་ཐོའི་ཨང་གྲངས་འདྲི་རྩད།',
      login: 'ཐོ་འཇུག་',
      reset: 'བསྐྱར་སྒྲིག་།',
      verify_wait: 'ཚོད་ལྟས་ར་སྤྲོད་བྱེད་བཞིན་པའི་སྒང་།, ཅུང་ཙམ་སྒུག་རོགས།...',
      enter_phone: 'རོགས་།ཁྱེད་རང་གི་ཁ་པར་ཨང་གྲངས་ནང་འཇུག་།',
      phone_format_error: 'ཁ་པར་ཨང་གྲངས་ཀྱི་རྣམ་གཞག་ཡང་དག་མིན་པ།',
      enter_security_code: 'ར་སྤྲོད་ཨང་ནང་འཇུག་བྱེད་རོགས་།',
      send_security_code: 'ར་སྤྲོད་ཨང་གྲངས་བསྐུར།',
      QQ_login: 'QQཐོ་འཇུག་',
      weibo_login: 'དཔོད་ཆུང་ཐོ་འཇུག',
      dingding_login: 'གཟེར་གཟེར་ཐོ་འཇུག་',
      first_install_ukey: 'རོགས་།སྔོན་ལ་སྒྲིག་སྦྱོར་།Ukeyསྐུལ་འདེད་།！',
      back_account_login: 'རྩིས་ཐོའི་ཨང་གྲངས་ནང་འཇུག་ཕྱིར་གཤིགས།',
      QR_code_invalid: 'རྩ་གཉིས་ཨང་རྟགས་ནུས་པ་ཤོར་ཟིན་།',
      click_refresh: 'གསར་འདོན་གནོན་རོགས་།',
      WeChat_scan_login: 'སྐད་འཕྲིན་གྱིས་རྩ་གཉིས་ཨང་རྟགས་བཤེར་འབེབས་བྱས།',
      APP_scan_login: 'APPཡིས་རྩ་གཉིས་ཨང་རྟགས་བཤར་འབེབས་བྱས་ནས་ཐོ་འགོད་བྱས་པ།',
      auth_scan_login: 'འདུས་སྦྱོར་དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་རྩ་གཉིས་ཨང་རྟགས་བཤེར་འབེབས་ཐོ་འཇུག',
      account_login: 'རྩིས་ཐོའི་ཨང་གྲངས་ནང་འཇུག་བྱེད།',
      Qr_code_Login: 'རྩ་གཉིས་ཨང་རྟགས་ཐོ་འཇུག་',
      login_failure: 'ཐོ་འཇུག་ཕམ་།',
      verification_code_error: 'ར་སྤྲོད་ཨང་ནོར་འཁྲུལ་།',
      warn: 'གསལ་འདེབས།',
      send_sms_code_success: 'གྲུབ་འབྲས་ཐོབ་པའི་ངང་བསྐུར་བའི་འཕྲིན་ཐུང་ར་སྤྲོད་ཨང་།',
      ukey_insert: 'UKEYའཇུག་ཟིན་པ་།',
      ukey_pull: 'UKEYབཏོན་ཟིན་།',
      ukey_login_not_use: 'UEKYབཀོལ་སྤྱོད་མི་ཐུབ་།ཐོ་འཇུག་།, དོ་དམ་པར་འབྲེལ་བ་གནང་རོགས།！',
      query_fail: 'བཙལ་ནས་ཕམ་ཉེས་བྱུང་བ་།',
      not_find_use: 'བབ་མཚུངས་ཀྱི་སྤྱོད་མཁན་རྙེད་མ་བྱུང་།, གཞི་གྲངས་འཚོལ་ཞིབ་ཡང་དག་ཡིན་མིན་འཚོལ་རོགས་།！',
      information_portal: 'ཆ་འཕྲིན་སྒོ་།',
      browser_recommended: 'འོས་སྦྱོར འོས་སྦྱོར བཤར་ཆས།',
  
      //指纹登录
      finger_scan_login: 'མཛུབ་རིས་བཤར་འབེབས་ཐོ་འཇུག་།',
      finger_login_step1: 'སྒྲིག་ཆས་འབྲེལ་མཐུད་བྱས་མེད།',
      finger_login_step2: 'མཛུབ་མོ་གནོན་རོགས་།',
      finger_login_step3: 'མཛུབ་མོ་ཡར་བཏེགས་།',
      finger_login_step4: 'པར་རིས་འཚོལ་བསྡུ་གྲུབ་འབྲས་ཐོབ་པའི་ངང་།',
      finger_login_step5: 'མཛུབ་རིས་འཚོལ་བསྡུ་གནས་ལེགས་གྲུབ་།',
      finger_login_step6: 'མཛུབ་རིས་ཐོ་འགོད་ཀྱི་ཁྱད་རྟགས་གནས་ལེགས་གྲུབ་བྱུང་བ།',
      finger_match_fail: 'མཛུབ་རིས་ཟླ་སྒྲིག་ཕམ་སོང་།, རོགས་།མཛུབ་རིས་བསྐྱར་དུ་སྡེབ་སྒྲིག་གམ་ཡང་ན་འཚོལ་བསྡུ་།!',
      browser_not_ws: 'བཤར་ཆས་ཀྱིས་wsགྲོས་མཐུན་ལ་རྒྱབ་སྐྱོར་མི་བྱེད་པ་།, རོགས་།བཤར་ཆས་IEབེད་སྤྱོད་།',
      connect_usb_fail: 'USBའབྲེལ་མཛུབ་རིས་དཔྱད་ཆས་ཕམ་སོང་།',
      open_usb_fail: 'USBམཛུབ་རིས་དཔྱད་ཆས་ཁ་ཕྱེ་ནས་ཕམ་ཁ་བྱུང་བའོ།།',
      connect_finger_fail: 'འབྲེལ་མཛུབ་རིས་དཔྱད་ཆས་།དུས་བརྒལ་།',
      change_browser: 'མེ་ཝ་བཤར་ཆས་ལ་རྒྱབ་སྐྱོར་མི་བྱེད།, བཤར་ཆས་གཞན་དག་བརྗེ་རོགས་།!',
      collect_finger_fail: 'མཛུབ་རིས་འཚོལ་བསྡུ་གནས་ཕམ་པའི་།',
      register_finger_fail: 'མཛུབ་རིས་ཀྱི་ཁྱད་རྟགས་ཐོ་འགོད་བྱེད་པར་ཕམ་ཉེས་བྱུང་བ།',
  
  
      //Ukey登录
      enter_pin_code: 'PINཨང་གྲངས་ནང་འཇུག་བྱེད་རོགས་།',
      ie_insert_ukey: 'IEབཤར་ཆས་འོག་ཏུ་འཛུད་Ukeyརྗེས་།དྲ་ངོས་གསར་པ་བཟོ་དགོས་།',
      not_check_device: 'སྒྲིག་ཆས་ལ་ཞིབ་དཔྱད་ཚད་ལེན་བྱེད་མ་ཐུབ་།',
  
      //页脚
      company: 'མཉམ་འབྲེལ་དབྱི་ཚན་རྩལ་ཚད་ཡོད་ཀུང་སི།',
      copyright_company: 'པར་དབང་ཡོད་ཚད།@མཉམ་བཞུགས་སློབ་ཆེན།',
      login_pageInfo_4: 'གཅིག་གྱུར་གྱི་ཐོབ་ཐང་དཔང་བདེན་ར་སྤྲོད་སྟེགས་བུ།-དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལྟེ་གནས་།',
  
      //页头
      person_center: 'མི་སྒེར་ལྟེ་གནས།',
      setting: 'སྒྲིག་འགོད་',
      exit_login: 'ཕྱིར་འཐེན་ཐོ་འཇུག་།',
      change_theme: 'བརྗོད་བྱ་གཙོ་བོའི་བརྗེ་བརྗེས་།',
  
      //再次登录
      tip_encrypted_phone: 'དྲོ་སྐྱིད་གསལ་འདེབས།: གསང་སྲུང་ཚོད་ལྟས་ར་སྤྲོད་དམ་ཡང་ན་ཁ་པར་གྱིས་ཚོད་ལྟས་ར་སྤྲོད།',
      security_setting: 'བདེ་འཇགས་སྒྲིག་བཀོད།',
      verify_way: 'ཚོད་ལྟས་ར་སྤྲོད་བྱེད་ཐབས།',
      select_verify_way: 'ར་སྤྲོད་བྱེད་སྟངས་འདེམས་རོགས་།',
      phone_verify: 'ལག་ཐོགས་ཁ་པར་གྱི་ཞིབ་བཤེར།',
      encrypted_verify: 'གསང་སྲུང་ཚོད་ལྟས་ར་སྤྲོད།',
      security_code: 'ར་སྤྲོད་ཨང་།',
      encrypted_question: 'གསང་སྲུང་གནད་དོན།',
      select_encrypted_question: 'གསང་བ་སྲུང་བའི་གནད་དོན་འདེམས་རོགས་།',
      question_answer: 'གནད་དོན་གྱི་ལན།',
      question_answer_not_empty: 'དྲི་བའི་དྲིས་ལན་སྟོང་པར་འཇོག་མི་ཉན།',
      confirm: 'གཏན་འཁེལ་བྱེད།',
      auth_fail: 'ཚོད་ལྟས་ར་སྤྲོད་ཕམ་།',
      bind_phone: 'ཁ་པར་ཨང་གྲངས་སྦྲེལ་རོགས།',
      bind_email: 'ཡིག་སྒམ་དང་སྦྲེལ་རོགས་།',
      tip_romote_login: 'ས་ཆ་གཞན་གྱི་ཐོ་འཇུག་གསལ་བརྡ།དེ་ནི་ཁྱེད་རང་གི་རྒྱུན་སྤྱོད་མིན་པའི་ཐོ་འཇུག་IPཡི་ས་གནས་རེད།ཁྱེད་རང་གི་གསང་བའི་ཁག་ཐེག་གམ་ཡང་ན་ལག་འཁྱེར་ཁ་པར་ར་སྤྲོད་གནང་རོགས།',
      romote_login: 'ཡུལ་གཞན་དུ་ཐོ་འགོད།',
      flag_romote_login: 'ཐོ་འཇུག་IPརྟགས་དེ་ནི་རྒྱུན་སྤྱོད་IP།',
  
  
      //登录绑定QQ
      bind_QQ_tip1: 'དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལས་སྟེགས་ཀྱི་ཨང་གྲངས་སྦྲེལ་ཐུབ་སོང་།: QQའདི་ཐེངས་དང་པོར་ཐོ་འཇུག་དང་བེད་སྤྱོད་།, དག་བཤེར་དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལྟེ་གནས་ཀྱི་རྩིས་ཨང་གསང་ཨང་།, དག་བཤེར་ལེགས་གྲུབ་བྱུང་རྗེས་ལྟོས་ཟླའི་ཨང་གྲངས་སྦྲེལ་ཆོག。',
      bind_QQ_tip2: 'དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལྟེ་གནས་ཀྱི་རྩིས་ཐོའི་ཨང་གྲངས།',
      bind_QQ_tip3: 'དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལྟེ་གནས་ཀྱི་གསང་གྲངས།',
      save: 'ཉར་ཚགས་བྱེད།',
      QQ_bind: 'QQབསྡམས་བཀྱིག་བྱས།',
  
      //登录绑定微博
      bind_WeiBo_tip1: 'དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལས་སྟེགས་ཀྱི་ཨང་གྲངས་སྦྲེལ་ཐུབ་སོང་།: དཔོད་ཆུང་འདི་ཐེངས་དང་པོར་ཐོ་འཇུག་དང་བེད་སྤྱོད་།, དག་བཤེར་དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལྟེ་གནས་ཀྱི་རྩིས་ཨང་གསང་ཨང་།, དག་བཤེར་ལེགས་གྲུབ་བྱུང་རྗེས་ལྟོས་ཟླའི་ཨང་གྲངས་སྦྲེལ་ཆོག, ཐེངས་རྗེས་མར་བཀོལ་སྤྱོད་དཔོད་ཆུང་ཐོ་འཇུག་བྱེད་སྐབས་ཐད་ཀར་དུ་དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལྟེ་གནས་།。',
      WeiBo_bind: 'དཔོད་ཆུང་སྦྲེལ་ཐུབ་སོང་།',
      //登录绑定钉钉
      bind_DingDing_tip1: 'དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལས་སྟེགས་ཀྱི་ཨང་གྲངས་སྦྲེལ་ཐུབ་སོང་།：གཟེར་གཟེར་དེ་ཐེངས་དང་པོར་ཐོ་འཇུག་དང་བེད་སྤྱོད་བྱེད།，དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལྟེ་གནས་ཀྱི་རྩིས་ཐོའི་ཨང་གྲངས་དང་གསང་གྲངས་དགོས་།དག་བཤེས་།，དག་བཤེར་ལེགས་གྲུབ་བྱུང་རྗེས་ལྟོས་ཟླའི་ཨང་གྲངས་སྦྲེལ་ཆོག，ཐེངས་རྗེས་མའི་བེད་སྤྱོད་གཅུས་གཟེར་ཐོ་འཇུག་བྱེད་སྐབས་ཐད་ཀར་དུ་དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལྟེ་གནས་།。',
      DingDing_bind: 'གཅུས་གཟེར་སྦྲེལ་ཐུབ་སོང་།',
  
      //登录绑定微信
      bind_WeChat_tip1: 'དྲོ་སྐྱིད་གསལ་འདེབས།: ཁྱེད་རང་གི་ཁེ་ལས་བརྒྱུད་དེ་འཕྲིན་ཆུང་དང་ཡང་ན་འཕྲིན་ཆུང་རྩ་གཉིས་ཨང་རྟགས་བཤར་འབེབས་།, མིག་སྔའི་ཐོ་འགོད་དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ཀྱི་ཨང་གྲངས་སྦྲེལ་དགོས།，གྲུབ་འབྲས་ཐོབ་པའི་ངང་སྦྲེལ་ཐུབ་རྗེས།，ཁྱེད་རང་གི་རྗེས་སུ་སྐད་འཕྲིན་བརྒྱུད་ཡང་ན་ཁེ་ལས་སྐད་འཕྲིན་གྱི་རྩ་གཉིས་ཨང་རྟགས་བཤར་འབེབས་དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་།、རྩ་གཉིས་ཨང་རྟགས་བཤར་འབེབས་གསང་གྲངས་འཚོལ་བ་སོགས་ཀྱི་བྱེད་ལས་།。དོ་སྣང་བྱོས།：སྔོན་ལ་དོ་སྣང་གནང་རོགས་།ཁེ་ལས་ཀྱི་སྐད་འཕྲིན་རྗེས་ཀྱི་རྩ་གཉིས་ཨང་རྟགས་བཤར་འབེབས་སྦྲེལ་།',
      bind_WeChat_tip2: 'འཕྲིན་ཕྲན་/ཁེ་ལས་སྐད་འཕྲིན་གྱི་རྩ་གཉིས་ཨང་རྟགས་བཤར་འབེབས་བྱས་ནས་བསྡམས་བཀྱིག་བྱས།',
  
      //登录校验
      login_check_tip1: 'གསང་གྲངས་བཙུགས་ནས་སྲུང་སྐྱོབ་བྱེད།: ཁྱེད་རང་ལ་ཕེབས་པར་དགའ་བསུ་ཞུ་།，',
      login_check_tip2: '，ཁྱེད་རང་གི་གསང་བའི་གནད་དོན་དང་དྲིས་ལན་འབྲི་རོགས་།，ཉར་ཚགས་ལེགས་གྲུབ་བྱུང་རྗེས།，གསང་བ་ཕྱིར་རྙེད་པའི་གསང་གྲངས་དང་ཐོ་འགོད་ཚོད་ལྟས་ར་སྤྲོད་སོགས་ཀྱི་ནུས་པ་བཀོལ་ཆོག。',
      login_check_tip3: 'ལག་ཐོགས་ཁ་པར་གྱི་ཚོད་ལྟས་ར་སྤྲོད་སྦྲེལ་ཐུབ་སོང་།: ཁྱེད་རང་ལ་ཕེབས་པར་དགའ་བསུ་ཞུ་།，',
      login_check_tip4: '，ཁྱེད་རང་གི་ཁ་པར་ཨང་གྲངས་འབྲི་རོགས་།, འདི་གནོན་ནས་ར་སྤྲོད་ཨང་གྲངས་བསྐུར།, མ་ལག་གིས་ཁྱེད་རང་གི་ཁ་པར་ལ་འཕྲིན་ཐུང་བསྐུར་གྱི་རེད།, ཁྱེད་རང་གི་འཕྲིན་ཐུང་ནང་དོན་ནང་གི་ར་སྤྲོད་ཨང་ནང་འཇུག་དགོས་།, ར་སྤྲོད་ལ་བརྟེན་ནས་།',
      login_check_tip5: 'ཡིག་སྒམ་ར་སྤྲོད་སྦྲེལ་ཐུབ་སོང་།：ཁྱེད་རང་ལ་ཕེབས་པར་དགའ་བསུ་ཞུ་།，',
      login_check_tip6: '，ཁྱེད་རང་གི་ཡིག་སྒམ་འབྲི་རོགས་།, འདི་གནོན་ནས་ར་སྤྲོད་ཨང་གྲངས་བསྐུར།, མ་ལག་གིས་ཁྱེད་རང་གི་ཡིག་སྒམ་ལ་སྦྲག་རྫས་བསྐུར་།, ཁྱེད་རང་ལ་སྦྲག་རྫས་ནང་དོན་ནང་གི་ར་སྤྲོད་ཨང་ནང་འཇུག་བྱ་དགོས་།, ར་སྤྲོད་ལ་བརྟེན་ནས་།',
      first_teacher: 'ཁྱེད་རང་གི་དགེ་རྒན་ཨང་དང་པོའི་མིང་ལ་ཅི་ཟེར་།',
      library_card_number: 'ཁྱེད་རང་གི་དཔེ་དེབ་བྱང་བུའི་ཨང་གྲངས་ནི་ཅི་ཞིག་།',
      common_QQ: 'ཁྱེད་རང་གི་རྒྱུན་སྤྱོད་ཀྱི་QQཨང་གྲངས་ནི་ག་ཚོད་།',
      first_phone: 'ཁྱེད་རང་གི་ཁ་པར་ཨང་གྲངས་དང་པོ་ནི་ག་ཚོད་།',
      luck_number: 'ཁྱེད་རང་གི་རླུང་རྟ་དར་བའི་གྲངས་ཀ་ནི་ག་ཚོད་།',
      custom_question: 'རང་གིས་མཚན་ཉིད་འཇོག་པའི་གནད་དོན།',
      custom_question_not_empty: 'ངེས་པར་དུ་རང་གིས་མཚན་ཉིད་འཇོག་པའི་གནད་དོན་ཡོད་དགོས།',
      phone: 'ཁ་པར་ཨང་གྲངས།',
      check: 'དག་བཤེར།',
      email: 'ཡིག་སྒམ་།',
      enter_email: 'ཡིག་སྒམ་ནང་འཇུག་བྱེད་རོགས་།',
      email_format_error: 'ཡིག་སྒམ་གྱི་རྣམ་བཞག་ཡང་དག་མ་རེད།',
      send_email_code_success: 'གྲུབ་འབྲས་ཐོབ་པའི་ངང་བསྐུར་ཡིག་སྒམ་ར་སྤྲོད་ཨང་།',
      send_sms_code_fail: 'འཕྲིན་ཐུང་བསྐུར་བའི་ར་སྤྲོད་ཨང་གྲངས་ཕམ་སོང་།',
      send_email_code_fail: 'ཡིག་སྒམ་ར་སྤྲོད་ཨང་གྲངས་བསྐུར་ཐུབ་མ་སོང་།',
      encrypted_bind: 'གསང་པའོ་སྦྲེལ་ཐུབ་སོང་།',
      encrypted_bind_fail: 'གསང་གྲངས་སྦྲེལ་ཐུབ་མ་སོང་།！',
      phone_bind: 'ཁ་པར་ཨང་གྲངས་བསྡམས་བཀྱིག་བྱས།',
      phone_bind_fail: 'ཁ་པར་ཨང་གྲངས་བསྡམས་བཀྱིག་ཕམ་སོང་།！',
      email_bind: 'ཡིག་སྒམ་སྦྲེལ་ཐུབ་སོང་།',
      email_bind_fail: 'ཡིག་སྒམ་བསྡམས་བསྡམས་ནས་ཕམ་སོང་།！',
  
      //登录错误
      login_error_tip1: 'འཚམས་འདྲི་དང་ལེན་མ་བྱས་།！',
      login_error_tip2: 'སྲིད་པའི་རྒྱུ་མཚན་ནི་།',
      login_error_tip3: 'ཁྱེད་རང་གི་མ་ལག་དེར་འཚམས་འདྲི་བྱེད་པའི་དབང་ཆ་མེད་།',
      login_error_tip4: 'ཁྱེད་རང་འཚམས་འདྲི་བྱེད་པའི་ས་གནས་མི་འགྲིག་།',
      login_error_tip5: 'གལ་ཏེ་གནད་དོན་གང་རུང་ཡོད་ཚེ།, དུས་ཐོག་ཏུ་འབྲེལ་བ་དོ་དམ་པ་ཐག་གཅོད་རོགས་།',
      login_error_tip6: 'ཁྱེད་རང་གི་ད་དུང་།',
      login_error_tip7: 'ཡང་བསྐྱར་ཐོ་འཇུག་བྱེད་པའམ་ཅུང་ཙམ་འགོར་རྗེས་ཚོད་ལྟ་བྱེད།。',
  
      //登录未授权
      login_unAuthorize_tip1: 'ཉེར་སྤྱོད་ཐོ་འགོད་བྱས་མེད།！',
      login_unAuthorize_tip2: 'བཀོལ་སྤྱོད་ལ་དབང་ཆ་མ་སྤྲད་པ།！',
      login_unAuthorize_tip3: 'ཉེར་སྤྱོད་དེ་རིགས་དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་ལས་སྟེགས་སུ་ཐོ་འགོད་བྱས་མེད།',
      login_unAuthorize_tip4: 'ཁྱོད་ཀྱིས་བཀོལ་སྤྱོད་དེ་ལ་འཚམས་འདྲི་བྱེད་པའི་དབང་ཆ་མེད་།',
      login_unAuthorize_tip5: 'གལ་ཏེ་གནད་དོན་གང་རུང་ཡོད་ཚེ།, དུས་ཐོག་ཏུ་འབྲེལ་བ་དོ་དམ་པ་ཐག་གཅོད་རོགས་།',
      login_unAuthorize_tip6: 'ཁྱེད་རང་གི་ད་དུང་།',
      login_unAuthorize_tip7: 'བསྐྱར་དུ།',
      login_unAuthorize_tip8: 'ཐོ་འཇུག་ཡང་ན་ཅུང་ཙམ་འགོར་རྗེས་ཡང་བསྐྱར་ཚོད་ལྟ་ཞིག་།',
  
      //第一次登录
      first_login_tip1: 'དྲོ་སྐྱིད་གསལ་འདེབས།: རྩིས་ཐོའི་ཨང་གྲངས་འདི་ཐེངས་དང་པོར་ཐོ་འཇུག་བྱེད་པའམ་ཡང་ན་གསང་གྲངས་དུས་ལས་ཡོལ་།, ངེས་པར་དུ་ཡང་བསྐྱར་གསང་གྲངས་བཟོ་དགོས།, གསང་གྲངས་གསར་པ་དང་ཐོག་མའི་གསང་གྲངས་གཅིག་པ་མ་རེད།,',
      first_login_tip2: 'གསང་གྲངས་ནི་ཡིག་རྟགས་',
      first_login_tip3: 'ལས་གྲུབ་པ་།, ཡིག་གཟུགས་ཆེ་ཆུང་གི་དབྱེ་བ་འབྱེད་དགོས།（མ་མཐར་ཡང་གྲངས་ཀ་',
      first_login_tip4: 'ཚུད་།、དབྱངས་གསལ་ཡི་གེ་',
      first_login_tip5: 'ཚུད་།、དེའི་ནང་དུ་དམིགས་བསལ་གྱི་ཡིག་རྟགས་',
      first_login_tip6: '།, སྟོང་ཆ་འདུས་མི་ཐུབ།）དབྱིན་ཡིག་གི་གསལ་བྱེད་དང་གྲངས་ཀའམ་མཚོན་རྟགས་ཀྱི་མཉམ་བསྲེས་གསང་ཨང་བཀོལ་བའི་བསམ་འཆར་འདོན།',
      new_pass: 'གསང་གྲངས་གསར་བ།',
      enter_new_pass: 'གསང་ཨང་གསར་པ་ནང་འཇུག་བྱེད་རོགས་།',
      pass_class: {
        strong: 'སྟོབས་ཆེ་།',
        middle: 'སྤྱིར་བཏང་གི་།',
        weak: 'ཞན་པ།'
      },
      confirm_pass: 'གཏན་འཁེལ་གསང་ཨང་།',
      enter_confirm_pass: 'གསང་གྲངས་ནང་འཇུག་རོགས་།',
      change_password: 'གསང་གྲངས་བཟོ་བཅོས་བྱེད།',
      change_password_fail: 'གསང་གྲངས་བཟོ་བཅོས་ཕམ་སོང་།！',
      the_two_passwords_are_not_the_same: 'ཐེངས་གཉིས་ནང་འཇུག་བྱས་པའི་གསང་གྲངས་གཅིག་པ་མ་རེད།!',
      password_length_error1: 'གསང་གྲངས་ཀྱི་རིང་ཚད་ནོར་བ།, གསང་ཨང་གི་རིང་ཚད་ཕལ་ཆེར་',
      password_length_error2: 'དང་',
      password_length_error3: 'བར་།！',
      password_error_digits1: 'གསང་ཨང་མ་མཐར་ཡང་གྲངས་ཀ་',
      password_error_digits2: 'འདུས་ཡོད་།!',
      password_error_letters1: 'གསང་ཨང་ཉུང་མཐར་ཡང་ཡིག་འབྲུ་',
      password_error_letters2: 'ཚུད་།!',
      password_error_specialchar1: 'གསང་ཨང་དགོས་།ཉུང་མཐར་ཡང་མི་',
      password_error_specialchar2: 'ཚུད་པའི་དམིགས་བསལ་གྱི་ཡིག་རྟགས་།!',
      password_without_whitespace: 'གསང་གྲངས་ནང་སྟོང་ཆ་ཚུད་མི་རུང་།',
  
      //登录提交
      reject: 'དང་ལེན་མི་བྱེད་པ།',
      warm_prompt: 'དྲོ་སྐྱིད་གསལ་འདེབས།',
  
      //注销
      logout_fail: 'ཐོ་གསུབ་ཕམ་སོང་།',
      logout_ticket_fail: 'འཛིན་ཤོག་ཐོ་ཁོངས་ནས་སུབ་རྒྱུ་ཕམ་པ།',
  
      //微信扫码
      loading_wait: 'ཁུར་སྣོན་བྱེད་བཞིན་པའི་སྒང་ཡིན་པའོ།།, ཅུང་ཙམ་འགོར་རྗེས་།...',
      Qr_code_invalid_scan: 'རྩ་གཉིས་ཨང་རྟགས་འདི་དུས་ལས་ཡོལ་།, ཡང་བསྐྱར་བཤར་འབེབས་རོགས་།',
      WeChat_scan_tip1: 'ཁྱེད་རང་གི་ད་དུང་དོ་ཁུར་བྱས་མེད་།སྐད་འཕྲིན་ཁེ་ལས་ཨང་གྲངས་།, རོགས་།རི་མོའི་སྟེང་གི་རྩ་གཉིས་ཨང་རྟགས་ལ་གཞིགས་ནས་དོ་ཁུར་བྱས་།',
      binding_success: 'བསྡམ་བཀྱིག་ལེགས་གྲུབ་བྱུང་།',
      login_success: 'ཐོ་འཇུག་གྲུབ་འབྲས་ཐོབ་པའི་ངང་།',
      login_name_not_empty: 'ཐོ་འཇུག་མིང་སྟོང་པ་ཡིན་མི་རུང་།',
      pass_not_empty: 'གསང་གྲངས་སྟོང་བ་ཡིན་མི་རུང་།',
      account_pass: 'རྩིས་ཨང་གི་གསང་གྲངས།',
      phone_code: 'ལག་ཐོགས་ཁ་པར་གྱི་ར་སྤྲོད་ཨང་།',
      confirm_login: 'ཐོ་འཇུག་ལ་གཏན་འཁེལ་བྱེད།',
      cancel_login: 'ཐོ་འཇུག་ཕྱིར་འཐེན་།',
      binding_account_yet: 'ཁྱོད་ཀྱིས་རྩིས་ཨང་ལ་སྦྲེལ་ཡོད་པ་རྟགས་བཤེར་བྱེད།',
      WeChat_scan_tip2: 'ཐོག་མའི་ཐོ་འགོད་ཟིན་ཐོ་འགོད་པ་རོགས་།དཔང་དངོས་བདེན་པ་ཡིན་པའི་ར་སྤྲོད་སྟེགས་བུའི་རྩིས་ཐོའི་ཨང་གྲངས་དང་གསང་བའི་ཨང་གྲངས་ནང་འཇུག་སྦྲེལ་མཐུད་།',
      is_binding_account: 'རྩིས་ཐོའི་ཨང་གྲངས་སྦྲེལ་དགོས་སམ་མི་དགོས་།',
      confirm_binding: 'གཏན་འཁེལ་སྦྲེལ་ཐུབ་སོང་།',
      cancel_binding: 'སྦྲེལ་མེད་པར་བཟོས།',
      WeChat_scan_tip3: 'ཨང་གྲངས་ལ་ཞིབ་བཤེར་བྱས་ནས་འཆིང་སྒྲིག་བྱས།, སྐད་འཕྲིན་གཞན་དག་བརྗེས་རོགས་།སྦྲེལ་།',
      WeChat_bind: 'སྐད་འཕྲིན་དང་སྦྲེལ།',
      self_bind_tip: 'ཁྲིམས་འགལ་གྱི་སྤྱོད་མཁན་དང་།འབྲེལ་གཏུག་བྱེད་རོགས་།དོ་དམ་པ་།',
  
      //同一人多账号
      user_account_select: 'སྤྱོད་མཁན་གྱི་རིགས་ཀྱི་རྩིས་ཐོའི་ཨང་གྲངས་འདེམས།',
      user_account_select_one: 'སྤྱོད་མཁན་གྱི་རིགས་ཤིག་འདེམ་རོགས་།རྩིས་ཐོའི་ཨང་གྲངས་ནི་གཏམ་མེད་ཁས་ལེན་གྱི་ཐོ་འཇུག་ཨང་གྲངས་།',
      user_account_select_tip_1: 'དྲོ་སྐྱིད་གསལ་འདེབས།：ཐོ་འཇུག་སྤྱོད་མཁན་རིགས་ཀྱི་རྩིས་ཐོའི་ཨང་གྲངས་གདམ་ག་བྱེད་རོགས་།，བདམས་ནས་སྤྱོད་མཁན་གྱི་རིགས་དབྱིབས་རྩིས་ཐོའི་ཨང་གྲངས་སྲིད་།',
      user_account_select_tip_2: 'གཏམ་མེད་ཁས་ལེན་གྱི་ཐོ་འཇུག་རྩིས་ཐོའི་ཨང་གྲངས།',
      user_account_select_tip_3: '，ཐེངས་རྗེས་མར་ཐོ་འཇུག་བྱེད་པའི་དུས་སུ་ཐད་ཀར་ཐོ་འཇུག་དང་གཏམ་མེད་ཁས་ལེན་གྱི་རྩིས་ཐོའི་ཨང་གྲངས་།！',
      user_account_select_tip_4: 'གལ་ཏེ་དེ་ལས་མང་བའི་སྤྱོད་མཁན་གྱི་རྩིས་ཐོའི་ཨང་གྲངས་རྙེད་མ་བྱུང་ན།, ཚོད་ལྟ་ཞིག་བྱས་ཆོག་།',
      user_account_select_tip_5: 'གཡས་གཡོན་ནས་འདྲེད་འགུལ་།',
      user_account_select_tip_6: 'སྤྱོད་མཁན་སྔར་ལས་མང་བའི་རིགས་དབྱིབས་ཀྱི་རྩིས་ཐོའི་ཨང་གྲངས་འཚོལ་།',
      user_account_select_tip_7: 'རྩིས་ཐོའི་ཨང་གྲངས།：',
      user_account_select_tip_8: 'ཐོབ་ཐང་།：',
    },
    //扫码微信登录输入框提示内容
    inputInfo: '请输入认证平台的账号',
    passwordInfo: '请输入认证平台的密码'
  }
  window.tip = {
    isLargeBg: false,//新版主题是否需要大背景图
    isChangeHttps: false,//是否转换为https，默认为false
    isHiddenReject: true,//是否隐藏入网承诺的拒绝按钮
    //入网承诺提示语
    // netCommitTips: null,
    isOpenMobileConsole: false,//是否开启移动端控制台调试
    isFouthThemeCenter: false,//主题居中开关
    isOpenResetBtn: false,//是否开启重置按钮
    isAppBtnFirst: false,//扫码登录底下的app切换按钮是否放在前面
    isFirstStyleLogoOutside: false,//新版第一套主题的logo是否放在登录框上方
    unlock: true, // 是否开启密码框小眼睛功能
    //登录框定制
    // loginLogoStyle: {
    //   width: 1200
    // },
    // loginBoxPosition: {
    //   top: 80,
    //   overflow:'hidden'
    // }
    // loginPage: 0  logo是否在内
    isRamdamBackground: false,//新版主题是否随机背景图
    backgroundUrlList: [
      '/assets/images/login/bg1.png',
      '/assets/images/login/bg2.jpg',
      // '/assets/images/login/bg3.jpg',
      // '/assets/images/login/bg4.jpg',
      // '/assets/images/login/bg5.jpg',
      // '/assets/images/login/bg6.jpg',
      // '/assets/images/login/bg7.jpg',
      // '/assets/images/login/bg8.jpg',
      // '/assets/images/login/bg9.jpg',
      // '/assets/images/login/bg10.jpg',
      // '/assets/images/login/bg11.jpg',
      // '/assets/images/login/bg12.jpg',
    ],
    logoIn: false,//新版主题登录框左边宽度与右边相同
    //顶部定制样式
    // loginLogoStyle:{
    //   width:'100%',
    //   boxSizing:'border-box',
    //   padding:'unset',
    // },
    // 顶部logo样式
    // logoStyle: {
    //   width: '100%'
    // },
    // 登录框定制样式
    // loginBoxPosition:{
    //   top: 120,
    //   width: '295px',
    //   background: 'rgba(248, 248, 248, 1)',
    // },
    // 页脚定制 --- 目前仅第二套
    // footerStyle: {
    //   background: 'rgba(224, 224, 224, 1)',
    //   padding: 10
    // }
    //页脚定制
    //移动端底部说明定制化
    // mobileBottomInfo: {
    //   infoStyle: {
    //     top: '0px',
    //     transform: 'unset'
    //   },
    //   infoText:'<div style="display: flex;width: 100%;justify-content: center;"><div style="width: 100px;height: 120px;display: block;background: red;margin-right: 10px;"><img style=""></div><div style="width: 160px;"><span style="font-weight: 700;">如何快速找回密码？</span><br>长按识别二维码或微信搜索“龙职人脸识别”小程序，可通过人脸识别快速修改登录密码。</div></div>'
    // }
    //新版登录页app下载显示
    // isShowAppDownload:true,
    // codeImg:'',
    // appDownName:'幼专'
    //新版登录页app下载显示
  }
  
