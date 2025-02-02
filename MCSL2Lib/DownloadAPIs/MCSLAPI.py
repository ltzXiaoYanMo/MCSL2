#     Copyright 2023, MCSL Team, mailto:lxhtt@vip.qq.com
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
"""
A function for communicatng with MCSLAPI.
"""

from typing import Callable

from PyQt5.QtCore import pyqtSignal, QThread

from MCSL2Lib.Controllers.networkController import MCSLNetworkSession, MCSLNetworkHeaders


class MCSLAPIDownloadURLParser:
    """URL设定器"""

    def __init__(self):
        pass

    @staticmethod
    def parseDownloaderAPIUrl():
        UrlArg = "https://api.mcsl.com.cn/DownloadAPI"
        TypeArg = [
            "/JavaDownloadInfo.json",
            "/SpigotDownloadInfo.json",
            "/PaperDownloadInfo.json",
            "/BungeeCordDownloadInfo.json",
            "/OfficialCoreDownloadInfo.json",
        ]
        rv = {}
        for i in range(len(TypeArg)):
            DownloadAPIUrl = UrlArg + TypeArg[i]
            (
                downloadFileTitles,
                downloadFileURLs,
                downloadFileNames,
                downloadFileFormats,
            ) = MCSLAPIDownloadURLParser.decodeDownloadJsons(DownloadAPIUrl)
            rv.update(
                {
                    i: dict(
                        zip(
                            (
                                "downloadFileTitles",
                                "downloadFileURLs",
                                "downloadFileNames",
                                "downloadFileFormats",
                            ),
                            (
                                downloadFileTitles,
                                downloadFileURLs,
                                downloadFileNames,
                                downloadFileFormats,
                            ),
                        )
                    )
                }
            )
        return rv

    @staticmethod
    def decodeDownloadJsons(RefreshUrl):
        downloadFileTitles = []
        downloadFileURLs = []
        downloadFileFormats = []
        downloadFileNames = []
        try:
            DownloadJson = MCSLNetworkSession().get(url=RefreshUrl, headers=MCSLNetworkHeaders)
        except Exception:
            return -2, -2, -2, -2
        try:
            PyDownloadList = DownloadJson.json()["MCSLDownloadList"]
            for i in PyDownloadList:
                downloadFileTitle = i["name"]
                downloadFileTitles.insert(0, downloadFileTitle)
                downloadFileURL = i["url"]
                downloadFileURLs.insert(0, downloadFileURL)
                downloadFileFormat = i["format"]
                downloadFileFormats.insert(0, downloadFileFormat)
                downloadFileName = i["filename"]
                downloadFileNames.insert(0, downloadFileName)
            return (
                downloadFileTitles,
                downloadFileURLs,
                downloadFileNames,
                downloadFileFormats,
            )
        except:
            return -1, -1, -1, -1


class FetchMCSLAPIDownloadURLThread(QThread):
    """
    用于获取网页内容的线程
    结束时发射fetchSignal信号，参数为url和data组成的元组
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, FinishSlot: Callable = None):
        super().__init__()
        self._id = None
        self.Data = None
        if FinishSlot is not None:
            self.fetchSignal.connect(FinishSlot)

    def run(self):
        self.fetchSignal.emit(MCSLAPIDownloadURLParser.parseDownloaderAPIUrl())

    def getData(self):
        return self.Data


class FetchMCSLAPIDownloadURLThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, _singleton=False, finishSlot=None) -> FetchMCSLAPIDownloadURLThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchMCSLAPIDownloadURLThread(finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchMCSLAPIDownloadURLThread(finishSlot)
