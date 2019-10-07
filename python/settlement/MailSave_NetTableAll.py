#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MailSaveTemple

MAX_MAIL_COUNT = 200

#预估值表
MailSaveTemple.SaveMailAttach("MailSave_PreNetTable", MAX_MAIL_COUNT, "E:\\data\\PreNetTable", 'PreNetTable')
#正式估值表
#MailSaveTemple.SaveMailAttach("MailSave_NetTable", MAX_MAIL_COUNT, "E:\\data\\NetTable", 'NetTable')
