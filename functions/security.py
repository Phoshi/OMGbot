# -*- coding: utf-8 -*-
def users():
	return [] #OMGbot Identified User [2]
def accessRight(user):
	accessRights={"PY":[]}
	if user in accessRights.keys():
		return accessRights[user]
	else:
		return []
