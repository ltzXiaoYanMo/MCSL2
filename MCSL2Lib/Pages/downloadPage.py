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
Download page with FastMirror and MCSLAPI.
"""

from os import path as osp, remove

from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QSizePolicy,
    QWidget,
    QFrame,
    QGridLayout,
    QVBoxLayout,
    QSpacerItem,
    QStackedWidget,
)
from qfluentwidgets import (
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel,
    Pivot,
    PushButton,
    FluentIcon as FIF,
    MessageBox,
    InfoBarPosition,
    InfoBar,
    StateToolTip,
    TransparentPushButton,
    TransparentTogglePushButton,
    VerticalSeparator,
    BodyLabel,
    HyperlinkButton,
)

from MCSL2Lib.Widgets.DownloadEntryViewerWidget import DownloadEntryBox
from MCSL2Lib.Widgets.DownloadProgressWidget import DownloadCard
from MCSL2Lib.DownloadAPIs.FastMirrorAPI import (
    FetchFastMirrorAPIThreadFactory,
    FetchFastMirrorAPICoreVersionThreadFactory,
)
from MCSL2Lib.Widgets.PolarsWidgets import PolarsTypeWidget
from MCSL2Lib.Widgets.FastMirrorWidgets import (
    FastMirrorBuildListWidget,
    FastMirrorCoreListWidget,
    FastMirrorVersionListWidget,
)
from MCSL2Lib.DownloadAPIs.MCSLAPI import FetchMCSLAPIDownloadURLThreadFactory
from MCSL2Lib.DownloadAPIs.PolarsAPI import (
    FetchPolarsAPICoreThreadFactory,
    FetchPolarsAPITypeThreadFactory,
)
from MCSL2Lib.DownloadAPIs.AkiraCloud import (
    FetchAkiraTypeThreadFactory,
    FetchAkiraCoreThreadFactory,
)
from MCSL2Lib.Controllers.aria2ClientController import Aria2Controller
from MCSL2Lib.Controllers.interfaceController import (
    ChildStackedWidget,
    MySmoothScrollArea,
)
from MCSL2Lib.Widgets.loadingTipWidget import (
    MCSLAPILoadingErrorWidget,
    MCSLAPILoadingWidget,
)
from MCSL2Lib.Controllers.settingsController import cfg
from MCSL2Lib.Widgets.singleMCSLAPIDownloadWidget import singleMCSLAPIDownloadWidget
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.Resources.icons import *
from MCSL2Lib.utils import openLocalFile  # noqa: F401
from MCSL2Lib.variables import (
    DownloadVariables,
    SettingsVariables,
)

downloadVariables = DownloadVariables()
settingsVariables = SettingsVariables()


@Singleton
class DownloadPage(QWidget):
    """下载页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # fmt: off
        self.fetchFastMirrorAPIThreadFactory = FetchFastMirrorAPIThreadFactory()
        self.fetchFastMirrorAPICoreVersionThreadFactory = FetchFastMirrorAPICoreVersionThreadFactory()

        self.fetchMCSLAPIDownloadURLThreadFactory = FetchMCSLAPIDownloadURLThreadFactory()

        self.fetchPolarsAPITypeThreadFactory = FetchPolarsAPITypeThreadFactory()
        self.fetchPolarsAPICoreThreadFactory = FetchPolarsAPICoreThreadFactory()

        self.fetchAkiraTypeThreadFactory = FetchAkiraTypeThreadFactory()
        self.fetchAkiraCoreThreadFactory = FetchAkiraCoreThreadFactory()
        # fmt: on
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")
        self.gridLayout_4 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout_4.addWidget(self.titleLabel, 0, 0, 1, 1)

        self.openDownloadFolderBtn = TransparentPushButton(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openDownloadFolderBtn.sizePolicy().hasHeightForWidth())
        self.openDownloadFolderBtn.setSizePolicy(sizePolicy)
        self.openDownloadFolderBtn.setObjectName("openDownloadFolderBtn")
        self.gridLayout_4.addWidget(self.openDownloadFolderBtn, 0, 1, 1, 1)

        self.openDownloadEntriesBtn = TransparentPushButton(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openDownloadEntriesBtn.sizePolicy().hasHeightForWidth())
        self.openDownloadEntriesBtn.setSizePolicy(sizePolicy)
        self.openDownloadEntriesBtn.setObjectName("openDownloadEntriesBtn")
        self.gridLayout_4.addWidget(self.openDownloadEntriesBtn, 0, 2, 1, 1)

        self.showDownloadingItemBtn = TransparentTogglePushButton(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showDownloadingItemBtn.sizePolicy().hasHeightForWidth())
        self.showDownloadingItemBtn.setSizePolicy(sizePolicy)
        self.showDownloadingItemBtn.setObjectName("showDownloadingItemBtn")
        self.gridLayout_4.addWidget(self.showDownloadingItemBtn, 0, 3, 1, 1)

        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")
        self.gridLayout_4.addWidget(self.subTitleLabel, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 3)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.downloadStackedWidget = QStackedWidget(self)
        self.downloadStackedWidget.setObjectName("downloadStackedWidget")

        self.downloadWithFastMirror = QWidget()
        self.downloadWithFastMirror.setObjectName("downloadWithFastMirror")

        self.gridLayout_2 = QGridLayout(self.downloadWithFastMirror)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.versionSubtitleLabel = SubtitleLabel(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.versionSubtitleLabel.setSizePolicy(sizePolicy)
        self.versionSubtitleLabel.setObjectName("versionSubtitleLabel")

        self.gridLayout_2.addWidget(self.versionSubtitleLabel, 0, 1, 1, 1)
        self.coreListSmoothScrollArea = MySmoothScrollArea(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreListSmoothScrollArea.sizePolicy().hasHeightForWidth())
        self.coreListSmoothScrollArea.setSizePolicy(sizePolicy)
        self.coreListSmoothScrollArea.setMinimumSize(QSize(200, 0))
        self.coreListSmoothScrollArea.setMaximumSize(QSize(200, 16777215))
        self.coreListSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.coreListSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.coreListSmoothScrollArea.setWidgetResizable(True)
        self.coreListSmoothScrollArea.setObjectName("coreListSmoothScrollArea")

        self.coreListScrollAreaWidgetContents = QWidget()
        self.coreListScrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 349))
        self.coreListScrollAreaWidgetContents.setObjectName("coreListScrollAreaWidgetContents")

        self.verticalLayout_14 = QVBoxLayout(self.coreListScrollAreaWidgetContents)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")

        self.coreListLayout = QVBoxLayout()
        self.coreListLayout.setObjectName("coreListLayout")

        self.verticalLayout_14.addLayout(self.coreListLayout)
        self.coreListSmoothScrollArea.setWidget(self.coreListScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.coreListSmoothScrollArea, 1, 0, 1, 1)
        self.buildSubtitleLabel = SubtitleLabel(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buildSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.buildSubtitleLabel.setSizePolicy(sizePolicy)
        self.buildSubtitleLabel.setObjectName("buildSubtitleLabel")
        self.gridLayout_2.addWidget(self.buildSubtitleLabel, 0, 2, 1, 1)
        self.coreListSubtitleLabel = SubtitleLabel(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreListSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.coreListSubtitleLabel.setSizePolicy(sizePolicy)
        self.coreListSubtitleLabel.setObjectName("coreListSubtitleLabel")
        self.gridLayout_2.addWidget(self.coreListSubtitleLabel, 0, 0, 1, 1)
        self.versionSmoothScrollArea = MySmoothScrollArea(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionSmoothScrollArea.sizePolicy().hasHeightForWidth())
        self.versionSmoothScrollArea.setSizePolicy(sizePolicy)
        self.versionSmoothScrollArea.setMinimumSize(QSize(160, 0))
        self.versionSmoothScrollArea.setMaximumSize(QSize(160, 16777215))
        self.versionSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.versionSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.versionSmoothScrollArea.setWidgetResizable(True)
        self.versionSmoothScrollArea.setObjectName("versionSmoothScrollArea")

        self.versionScrollAreaWidgetContents = QWidget()
        self.versionScrollAreaWidgetContents.setGeometry(QRect(0, 0, 170, 349))
        self.versionScrollAreaWidgetContents.setObjectName("versionScrollAreaWidgetContents")

        self.verticalLayout_13 = QVBoxLayout(self.versionScrollAreaWidgetContents)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        self.versionLayout = QVBoxLayout()
        self.versionLayout.setObjectName("versionLayout")

        self.verticalLayout_13.addLayout(self.versionLayout)
        self.versionSmoothScrollArea.setWidget(self.versionScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.versionSmoothScrollArea, 1, 1, 1, 1)
        self.refreshFastMirrorAPIBtn = PushButton(
            icon=FIF.UPDATE, text=self.tr("刷新"), parent=self.downloadWithFastMirror
        )
        self.refreshFastMirrorAPIBtn.setObjectName("refreshFastMirrorAPIBtn")

        self.gridLayout_2.addWidget(self.refreshFastMirrorAPIBtn, 0, 3, 1, 1)
        self.buildScrollArea = MySmoothScrollArea(self.downloadWithFastMirror)
        self.buildScrollArea.setMinimumSize(QSize(304, 0))
        self.buildScrollArea.setFrameShape(QFrame.NoFrame)
        self.buildScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.buildScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.buildScrollArea.setWidgetResizable(True)
        self.buildScrollArea.setObjectName("buildScrollArea")

        self.buildScrollAreaWidgetContents = QWidget()
        self.buildScrollAreaWidgetContents.setGeometry(QRect(0, 0, 346, 349))
        self.buildScrollAreaWidgetContents.setObjectName("buildScrollAreaWidgetContents")

        self.verticalLayout_2 = QVBoxLayout(self.buildScrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.buildLayout = QVBoxLayout()
        self.buildLayout.setObjectName("buildLayout")

        self.verticalLayout_2.addLayout(self.buildLayout)
        self.buildScrollArea.setWidget(self.buildScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.buildScrollArea, 1, 2, 1, 2)
        self.downloadStackedWidget.addWidget(self.downloadWithFastMirror)
        self.downloadWithMCSLAPI = QWidget()
        self.downloadWithMCSLAPI.setObjectName("downloadWithMCSLAPI")

        self.gridLayout_3 = QGridLayout(self.downloadWithMCSLAPI)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.MCSLAPIPivot = Pivot(self.downloadWithMCSLAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIPivot.sizePolicy().hasHeightForWidth())
        self.MCSLAPIPivot.setSizePolicy(sizePolicy)
        self.MCSLAPIPivot.setFixedSize(QSize(210, 45))
        self.MCSLAPIPivot.setObjectName("MCSLAPIPivot")

        self.gridLayout_3.addWidget(self.MCSLAPIPivot, 0, 0, 1, 1)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 1, 1, 1)
        self.MCSLAPIStackedWidget = ChildStackedWidget(self.downloadWithMCSLAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIStackedWidget.sizePolicy().hasHeightForWidth())
        self.MCSLAPIStackedWidget.setSizePolicy(sizePolicy)
        self.MCSLAPIStackedWidget.setMinimumSize(QSize(676, 336))
        self.MCSLAPIStackedWidget.setMaximumSize(QSize(16777215, 16777215))
        self.MCSLAPIStackedWidget.setObjectName("MCSLAPIStackedWidget")

        self.MCSLAPIJava = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIJava.sizePolicy().hasHeightForWidth())
        self.MCSLAPIJava.setSizePolicy(sizePolicy)
        self.MCSLAPIJava.setObjectName("MCSLAPIJava")

        self.verticalLayout_3 = QVBoxLayout(self.MCSLAPIJava)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.MCSLAPIJavaScrollArea = MySmoothScrollArea(self.MCSLAPIJava)
        self.MCSLAPIJavaScrollArea.setWidgetResizable(True)
        self.MCSLAPIJavaScrollArea.setObjectName("MCSLAPIJavaScrollArea")

        self.MCSLAPIJavaScrollAreaWidgetContents = QWidget()
        self.MCSLAPIJavaScrollAreaWidgetContents.setGeometry(QRect(0, 0, 698, 348))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLAPIJavaScrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.MCSLAPIJavaScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.MCSLAPIJavaScrollAreaWidgetContents.setObjectName(
            "MCSLAPIJavaScrollAreaWidgetContents"
        )

        self.verticalLayout_8 = QVBoxLayout(self.MCSLAPIJavaScrollAreaWidgetContents)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        self.MCSLAPIJavaScrollAreaLayout = QVBoxLayout()
        self.MCSLAPIJavaScrollAreaLayout.setObjectName("MCSLAPIJavaScrollAreaLayout")

        self.verticalLayout_8.addLayout(self.MCSLAPIJavaScrollAreaLayout)
        self.MCSLAPIJavaScrollArea.setWidget(self.MCSLAPIJavaScrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.MCSLAPIJavaScrollArea)
        self.MCSLAPIStackedWidget.addWidget(self.MCSLAPIJava)
        self.MCSLAPISpigot = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPISpigot.sizePolicy().hasHeightForWidth())
        self.MCSLAPISpigot.setSizePolicy(sizePolicy)
        self.MCSLAPISpigot.setObjectName("MCSLAPISpigot")

        self.verticalLayout_4 = QVBoxLayout(self.MCSLAPISpigot)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.MCSLAPISpigotScrollArea = MySmoothScrollArea(self.MCSLAPISpigot)
        self.MCSLAPISpigotScrollArea.setWidgetResizable(True)
        self.MCSLAPISpigotScrollArea.setObjectName("MCSLAPISpigotScrollArea")

        self.MCSLAPISpigotScrollAreaWidgetContents = QWidget()
        self.MCSLAPISpigotScrollAreaWidgetContents.setGeometry(QRect(0, 0, 698, 348))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLAPISpigotScrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.MCSLAPISpigotScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.MCSLAPISpigotScrollAreaWidgetContents.setObjectName(
            "MCSLAPISpigotScrollAreaWidgetContents"
        )

        self.verticalLayout_9 = QVBoxLayout(self.MCSLAPISpigotScrollAreaWidgetContents)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")

        self.MCSLAPISpigotScrollAreaLayout = QVBoxLayout()
        self.MCSLAPISpigotScrollAreaLayout.setObjectName("MCSLAPISpigotScrollAreaLayout")

        self.verticalLayout_9.addLayout(self.MCSLAPISpigotScrollAreaLayout)
        self.MCSLAPISpigotScrollArea.setWidget(self.MCSLAPISpigotScrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.MCSLAPISpigotScrollArea)
        self.MCSLAPIStackedWidget.addWidget(self.MCSLAPISpigot)
        self.MCSLAPIPaper = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIPaper.sizePolicy().hasHeightForWidth())
        self.MCSLAPIPaper.setSizePolicy(sizePolicy)
        self.MCSLAPIPaper.setObjectName("MCSLAPIPaper")

        self.verticalLayout_5 = QVBoxLayout(self.MCSLAPIPaper)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.MCSLAPIPaperScrollArea = MySmoothScrollArea(self.MCSLAPIPaper)
        self.MCSLAPIPaperScrollArea.setWidgetResizable(True)
        self.MCSLAPIPaperScrollArea.setObjectName("MCSLAPIPaperScrollArea")

        self.MCSLAPIPaperScrollAreaWidgetContents = QWidget()
        self.MCSLAPIPaperScrollAreaWidgetContents.setGeometry(QRect(0, 0, 698, 348))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLAPIPaperScrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.MCSLAPIPaperScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.MCSLAPIPaperScrollAreaWidgetContents.setObjectName(
            "MCSLAPIPaperScrollAreaWidgetContents"
        )

        self.verticalLayout_10 = QVBoxLayout(self.MCSLAPIPaperScrollAreaWidgetContents)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")

        self.MCSLAPIPaperScrollAreaLayout = QVBoxLayout()
        self.MCSLAPIPaperScrollAreaLayout.setObjectName("MCSLAPIPaperScrollAreaLayout")

        self.verticalLayout_10.addLayout(self.MCSLAPIPaperScrollAreaLayout)
        self.MCSLAPIPaperScrollArea.setWidget(self.MCSLAPIPaperScrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.MCSLAPIPaperScrollArea)
        self.MCSLAPIStackedWidget.addWidget(self.MCSLAPIPaper)
        self.MCSLAPIBungeeCord = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIBungeeCord.sizePolicy().hasHeightForWidth())
        self.MCSLAPIBungeeCord.setSizePolicy(sizePolicy)
        self.MCSLAPIBungeeCord.setObjectName("MCSLAPIBungeeCord")

        self.verticalLayout_6 = QVBoxLayout(self.MCSLAPIBungeeCord)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.MCSLAPIBungeeCordScrollArea = MySmoothScrollArea(self.MCSLAPIBungeeCord)
        self.MCSLAPIBungeeCordScrollArea.setWidgetResizable(True)
        self.MCSLAPIBungeeCordScrollArea.setObjectName("MCSLAPIBungeeCordScrollArea")

        self.MCSLAPIBungeeCordScrollAreaWidgetContents = QWidget()
        self.MCSLAPIBungeeCordScrollAreaWidgetContents.setGeometry(QRect(0, 0, 698, 348))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLAPIBungeeCordScrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.MCSLAPIBungeeCordScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.MCSLAPIBungeeCordScrollAreaWidgetContents.setObjectName(
            "MCSLAPIBungeeCordScrollAreaWidgetContents"
        )

        self.verticalLayout_11 = QVBoxLayout(self.MCSLAPIBungeeCordScrollAreaWidgetContents)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")

        self.MCSLAPIBungeeCordScrollAreaLayout = QVBoxLayout()
        self.MCSLAPIBungeeCordScrollAreaLayout.setObjectName("MCSLAPIBungeeCordScrollAreaLayout")

        self.verticalLayout_11.addLayout(self.MCSLAPIBungeeCordScrollAreaLayout)
        self.MCSLAPIBungeeCordScrollArea.setWidget(self.MCSLAPIBungeeCordScrollAreaWidgetContents)
        self.verticalLayout_6.addWidget(self.MCSLAPIBungeeCordScrollArea)
        self.MCSLAPIStackedWidget.addWidget(self.MCSLAPIBungeeCord)
        self.MCSLAPIOfficialCore = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIOfficialCore.sizePolicy().hasHeightForWidth())
        self.MCSLAPIOfficialCore.setSizePolicy(sizePolicy)
        self.MCSLAPIOfficialCore.setObjectName("MCSLAPIOfficialCore")

        self.verticalLayout_7 = QVBoxLayout(self.MCSLAPIOfficialCore)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.MCSLAPIOfficialCoreScrollArea = MySmoothScrollArea(self.MCSLAPIOfficialCore)
        self.MCSLAPIOfficialCoreScrollArea.setWidgetResizable(True)
        self.MCSLAPIOfficialCoreScrollArea.setObjectName("MCSLAPIOfficialCoreScrollArea")
        self.MCSLAPIOfficialCoreScrollAreaWidgetContents = QWidget()
        self.MCSLAPIOfficialCoreScrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLAPIOfficialCoreScrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.MCSLAPIOfficialCoreScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.MCSLAPIOfficialCoreScrollAreaWidgetContents.setObjectName(
            "MCSLAPIOfficialCoreScrollAreaWidgetContents"
        )

        self.verticalLayout_12 = QVBoxLayout(self.MCSLAPIOfficialCoreScrollAreaWidgetContents)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")

        self.MCSLAPIOfficialCoreScrollAreaLayout = QVBoxLayout()
        self.MCSLAPIOfficialCoreScrollAreaLayout.setObjectName(
            "MCSLAPIOfficialCoreScrollAreaLayout"
        )

        self.verticalLayout_12.addLayout(self.MCSLAPIOfficialCoreScrollAreaLayout)
        self.MCSLAPIOfficialCoreScrollArea.setWidget(
            self.MCSLAPIOfficialCoreScrollAreaWidgetContents
        )
        self.verticalLayout_7.addWidget(self.MCSLAPIOfficialCoreScrollArea)
        self.MCSLAPIStackedWidget.addWidget(self.MCSLAPIOfficialCore)
        self.gridLayout_3.addWidget(self.MCSLAPIStackedWidget, 1, 0, 1, 3)
        self.refreshMCSLAPIBtn = PushButton(
            icon=FIF.UPDATE, text=self.tr("刷新"), parent=self.downloadWithMCSLAPI
        )
        self.refreshMCSLAPIBtn.setObjectName("refreshMCSLAPIBtn")

        self.gridLayout_3.addWidget(self.refreshMCSLAPIBtn, 0, 2, 1, 1)
        self.downloadStackedWidget.addWidget(self.downloadWithMCSLAPI)

        self.downloadWithPolarsAPI = QWidget()
        self.downloadWithPolarsAPI.setObjectName("downloadWithPolarsAPI")

        self.gridLayout_5 = QGridLayout(self.downloadWithPolarsAPI)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.polarsCoreScrollArea = MySmoothScrollArea(self.downloadWithPolarsAPI)
        self.polarsCoreScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.polarsCoreScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.polarsCoreScrollArea.setWidgetResizable(True)
        self.polarsCoreScrollArea.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.polarsCoreScrollArea.setObjectName("polarsCoreScrollArea")

        self.polarsCoreScrollAreaContents = QWidget()
        self.polarsCoreScrollAreaContents.setGeometry(QRect(0, 0, 461, 331))
        self.polarsCoreScrollAreaContents.setObjectName("polarsCoreScrollAreaContents")

        self.gridLayout_7 = QGridLayout(self.polarsCoreScrollAreaContents)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.polarsCoreLayout = QVBoxLayout()
        self.polarsCoreLayout.setObjectName("polarsCoreLayout")

        self.gridLayout_7.addLayout(self.polarsCoreLayout, 0, 0, 1, 1)
        self.polarsCoreLayout = QVBoxLayout()
        self.polarsCoreLayout.setObjectName("polarsCoreLayout")

        self.gridLayout_7.addLayout(self.polarsCoreLayout, 0, 0, 1, 1)
        self.polarsCoreScrollArea.setWidget(self.polarsCoreScrollAreaContents)
        self.gridLayout_5.addWidget(self.polarsCoreScrollArea, 2, 2, 2, 2)
        self.polarsTypeLabel = SubtitleLabel(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarsTypeLabel.sizePolicy().hasHeightForWidth())
        self.polarsTypeLabel.setSizePolicy(sizePolicy)
        self.polarsTypeLabel.setObjectName("polarsTypeLabel")

        self.gridLayout_5.addWidget(self.polarsTypeLabel, 0, 2, 1, 1)
        self.VerticalSeparator_2 = VerticalSeparator(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VerticalSeparator_2.sizePolicy().hasHeightForWidth())
        self.VerticalSeparator_2.setSizePolicy(sizePolicy)
        self.VerticalSeparator_2.setMinimumSize(QSize(3, 0))
        self.VerticalSeparator_2.setMaximumSize(QSize(3, 16777215))
        self.VerticalSeparator_2.setObjectName("VerticalSeparator_2")

        self.gridLayout_5.addWidget(self.VerticalSeparator_2, 0, 1, 4, 1)
        self.refreshPolarsAPIBtn = PushButton(
            icon=FIF.UPDATE, text="刷新", parent=self.downloadWithPolarsAPI
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshPolarsAPIBtn.sizePolicy().hasHeightForWidth())
        self.refreshPolarsAPIBtn.setSizePolicy(sizePolicy)
        self.refreshPolarsAPIBtn.setObjectName("refreshPolarsAPIBtn")
        self.gridLayout_5.addWidget(self.refreshPolarsAPIBtn, 0, 3, 1, 1)
        self.polarsDescriptionLabel = BodyLabel(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarsDescriptionLabel.sizePolicy().hasHeightForWidth())
        self.polarsDescriptionLabel.setSizePolicy(sizePolicy)
        self.polarsDescriptionLabel.setObjectName("polarsDescriptionLabel")

        self.gridLayout_5.addWidget(self.polarsDescriptionLabel, 1, 2, 1, 2)
        self.polarsTypeScrollArea = MySmoothScrollArea(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarsTypeScrollArea.sizePolicy().hasHeightForWidth())
        self.polarsTypeScrollArea.setSizePolicy(sizePolicy)
        self.polarsTypeScrollArea.setMinimumSize(QSize(170, 0))
        self.polarsTypeScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.polarsTypeScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.polarsTypeScrollArea.setWidgetResizable(True)
        self.polarsTypeScrollArea.setObjectName("polarsTypeScrollArea")

        self.polarsTypeScrollAreaContents = QWidget()
        self.polarsTypeScrollAreaContents.setGeometry(QRect(0, 0, 200, 356))
        self.polarsTypeScrollAreaContents.setObjectName("polarsTypeScrollAreaContents")

        self.gridLayout_6 = QGridLayout(self.polarsTypeScrollAreaContents)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.polarsTypeLayout = QVBoxLayout()
        self.polarsTypeLayout.setObjectName("polarsTypeLayout")

        self.gridLayout_6.addLayout(self.polarsTypeLayout, 0, 0, 1, 1)
        self.polarsTypeScrollArea.setWidget(self.polarsTypeScrollAreaContents)
        self.gridLayout_5.addWidget(self.polarsTypeScrollArea, 1, 0, 3, 1)
        self.polarsTitle = SubtitleLabel(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarsTitle.sizePolicy().hasHeightForWidth())
        self.polarsTitle.setSizePolicy(sizePolicy)
        self.polarsTitle.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.polarsTitle.setObjectName("polarsTitle")

        self.gridLayout_5.addWidget(self.polarsTitle, 0, 0, 1, 1)
        self.downloadStackedWidget.addWidget(self.downloadWithPolarsAPI)
        self.downloadWithAkiraCloud = QWidget()
        self.downloadWithAkiraCloud.setObjectName("downloadWithAkiraCloud")

        self.gridLayout_10 = QGridLayout(self.downloadWithAkiraCloud)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.akiraTitle = SubtitleLabel(self.downloadWithAkiraCloud)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.akiraTitle.sizePolicy().hasHeightForWidth())
        self.akiraTitle.setSizePolicy(sizePolicy)
        self.akiraTitle.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.akiraTitle.setObjectName("akiraTitle")

        self.gridLayout_10.addWidget(self.akiraTitle, 0, 0, 1, 1)
        self.VerticalSeparator_3 = VerticalSeparator(self.downloadWithAkiraCloud)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VerticalSeparator_3.sizePolicy().hasHeightForWidth())
        self.VerticalSeparator_3.setSizePolicy(sizePolicy)
        self.VerticalSeparator_3.setMinimumSize(QSize(3, 0))
        self.VerticalSeparator_3.setMaximumSize(QSize(3, 16777215))
        self.VerticalSeparator_3.setObjectName("VerticalSeparator_3")

        self.gridLayout_10.addWidget(self.VerticalSeparator_3, 0, 1, 3, 1)
        self.akiraTypeLabel = SubtitleLabel(self.downloadWithAkiraCloud)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.akiraTypeLabel.sizePolicy().hasHeightForWidth())
        self.akiraTypeLabel.setSizePolicy(sizePolicy)
        self.akiraTypeLabel.setObjectName("akiraTypeLabel")

        self.gridLayout_10.addWidget(self.akiraTypeLabel, 0, 2, 1, 1)
        self.refreshAkiraCloudBtn = PushButton(
            icon=FIF.UPDATE, text=self.tr("刷新"), parent=self.downloadWithAkiraCloud
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshAkiraCloudBtn.sizePolicy().hasHeightForWidth())
        self.refreshAkiraCloudBtn.setSizePolicy(sizePolicy)
        self.refreshAkiraCloudBtn.setObjectName("refreshAkiraCloudBtn")

        self.gridLayout_10.addWidget(self.refreshAkiraCloudBtn, 0, 3, 1, 1)
        self.akiraTypeScrollArea = MySmoothScrollArea(self.downloadWithAkiraCloud)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.akiraTypeScrollArea.sizePolicy().hasHeightForWidth())
        self.akiraTypeScrollArea.setSizePolicy(sizePolicy)
        self.akiraTypeScrollArea.setMinimumSize(QSize(170, 0))
        self.akiraTypeScrollArea.setMaximumSize(QSize(170, 16777215))
        self.akiraTypeScrollArea.setFrameShape(QFrame.NoFrame)
        self.akiraTypeScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.akiraTypeScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.akiraTypeScrollArea.setWidgetResizable(True)
        self.akiraTypeScrollArea.setObjectName("akiraTypeScrollArea")

        self.akiraTypeScrollAreaContents = QWidget()
        self.akiraTypeScrollAreaContents.setGeometry(QRect(0, 0, 170, 351))
        self.akiraTypeScrollAreaContents.setObjectName("akiraTypeScrollAreaContents")

        self.gridLayout_9 = QGridLayout(self.akiraTypeScrollAreaContents)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.akiraTypeLayout = QVBoxLayout()
        self.akiraTypeLayout.setObjectName("akiraTypeLayout")

        self.gridLayout_9.addLayout(self.akiraTypeLayout, 0, 0, 1, 1)
        self.akiraTypeScrollArea.setWidget(self.akiraTypeScrollAreaContents)
        self.gridLayout_10.addWidget(self.akiraTypeScrollArea, 1, 0, 2, 1)
        self.akiraCoreScrollArea = MySmoothScrollArea(self.downloadWithAkiraCloud)
        self.akiraCoreScrollArea.setFrameShape(QFrame.NoFrame)
        self.akiraCoreScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.akiraCoreScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.akiraCoreScrollArea.setWidgetResizable(True)
        self.akiraCoreScrollArea.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.akiraCoreScrollArea.setObjectName("akiraCoreScrollArea")

        self.akiraCoreScrollAreaContents = QWidget()
        self.akiraCoreScrollAreaContents.setGeometry(QRect(0, 0, 491, 345))
        self.akiraCoreScrollAreaContents.setObjectName("akiraCoreScrollAreaContents")

        self.gridLayout_8 = QGridLayout(self.akiraCoreScrollAreaContents)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")

        self.akiraCoreLayout = QVBoxLayout()
        self.akiraCoreLayout.setObjectName("akiraCoreLayout")

        self.gridLayout_8.addLayout(self.akiraCoreLayout, 0, 0, 1, 1)
        self.akiraCoreScrollArea.setWidget(self.akiraCoreScrollAreaContents)
        self.gridLayout_10.addWidget(self.akiraCoreScrollArea, 2, 2, 1, 2)
        self.downloadStackedWidget.addWidget(self.downloadWithAkiraCloud)
        self.gridLayout.addWidget(self.downloadStackedWidget, 3, 2, 1, 1)

        self.VerticalSeparator = VerticalSeparator(self)
        self.VerticalSeparator.setObjectName("VerticalSeparator")

        self.gridLayout.addWidget(self.VerticalSeparator, 3, 3, 1, 1)

        self.downloadingItemWidget = MySmoothScrollArea(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadingItemWidget.sizePolicy().hasHeightForWidth())
        self.downloadingItemWidget.setSizePolicy(sizePolicy)
        self.downloadingItemWidget.setMinimumSize(QSize(310, 0))
        self.downloadingItemWidget.setMaximumSize(QSize(310, 16777215))
        self.downloadingItemWidget.setFrameShape(QFrame.NoFrame)
        self.downloadingItemWidget.setWidgetResizable(True)
        self.downloadingItemWidget.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.downloadingItemWidget.setObjectName("downloadingItemWidget")

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 310, 407))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.downloadingItemLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.downloadingItemLayout.setContentsMargins(0, 0, 0, 0)
        self.downloadingItemLayout.setObjectName("downloadingItemLayout")

        self.downloadingItemWidget.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.downloadingItemWidget, 3, 4, 1, 1)
        self.dsList = [
            self.downloadWithFastMirror,
            self.downloadWithMCSLAPI,
            self.downloadWithPolarsAPI,
            self.downloadWithAkiraCloud,
        ]
        self.downloadStackedWidget.setCurrentWidget(
            self.dsList[settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))]
        )

        self.setObjectName("DownloadInterface")

        self.titleLabel.setText(self.tr("下载"))
        self.subTitleLabel.setText(self.tr("Aria2引擎高速驱动！"))
        self.coreListSubtitleLabel.setText(self.tr("核心列表"))
        self.versionSubtitleLabel.setText(self.tr("游戏版本"))
        self.buildSubtitleLabel.setText(self.tr("构建列表"))
        self.refreshFastMirrorAPIBtn.setText(self.tr("刷新"))
        self.openDownloadFolderBtn.setText(self.tr("打开下载文件夹"))
        self.openDownloadEntriesBtn.setText(self.tr("打开下载记录"))
        self.showDownloadingItemBtn.setText(self.tr("展开下载中列表"))
        self.polarsTitle.setText("核心类型")
        self.akiraTitle.setText("核心类型")

        self.coreListSmoothScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.MCSLAPIPivot.addItem(
            routeKey="MCSLAPIJava",
            text=self.tr("Java环境"),
            onClick=lambda: self.MCSLAPIStackedWidget.setCurrentWidget(self.MCSLAPIJava),
        )
        self.MCSLAPIPivot.addItem(
            routeKey="MCSLAPISpigot",
            text=self.tr("Spigot核心"),
            onClick=lambda: self.MCSLAPIStackedWidget.setCurrentWidget(self.MCSLAPISpigot),
        )
        self.MCSLAPIPivot.addItem(
            routeKey="MCSLAPIPaper",
            text=self.tr("Paper核心"),
            onClick=lambda: self.MCSLAPIStackedWidget.setCurrentWidget(self.MCSLAPIPaper),
        )
        self.MCSLAPIPivot.addItem(
            routeKey="MCSLAPIBungeeCord",
            text=self.tr("BungeeCord代理"),
            onClick=lambda: self.MCSLAPIStackedWidget.setCurrentWidget(self.MCSLAPIBungeeCord),
        )
        self.MCSLAPIPivot.addItem(
            routeKey="MCSLAPIOfficialCore",
            text=self.tr("Vanilla核心"),
            onClick=lambda: self.MCSLAPIStackedWidget.setCurrentWidget(self.MCSLAPIOfficialCore),
        )
        self.MCSLAPILayoutList = [
            self.MCSLAPIJavaScrollAreaLayout,
            self.MCSLAPISpigotScrollAreaLayout,
            self.MCSLAPIPaperScrollAreaLayout,
            self.MCSLAPIBungeeCordScrollAreaLayout,
            self.MCSLAPIOfficialCoreScrollAreaLayout,
        ]
        self.MCSLAPIJavaScrollArea.setFrameShape(QFrame.NoFrame)
        self.MCSLAPISpigotScrollArea.setFrameShape(QFrame.NoFrame)
        self.MCSLAPIPaperScrollArea.setFrameShape(QFrame.NoFrame)
        self.MCSLAPIBungeeCordScrollArea.setFrameShape(QFrame.NoFrame)
        self.MCSLAPIOfficialCoreScrollArea.setFrameShape(QFrame.NoFrame)
        self.MCSLAPIPivot.setCurrentItem("MCSLAPIJava")
        self.MCSLAPIStackedWidget.currentChanged.connect(self.refreshDownloads)
        self.refreshMCSLAPIBtn.clicked.connect(self.getMCSLAPI)
        self.refreshPolarsAPIBtn.clicked.connect(self.getPolarsAPI)
        self.refreshFastMirrorAPIBtn.clicked.connect(self.getFastMirrorAPI)
        self.refreshMCSLAPIBtn.setEnabled(False)
        self.scrollAreaSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.openDownloadFolderBtn.setIcon(FIF.FOLDER)
        self.openDownloadFolderBtn.clicked.connect(lambda: openLocalFile(".\\MCSL2\\Downloads\\"))

        self.openDownloadEntriesBtn.setIcon(FIF.MENU)
        self.openDownloadEntriesBtn.clicked.connect(
            lambda: {
                (box := DownloadEntryBox(self)),
                box.show(),
                box.raise_(),
                box.asyncGetEntries(),
            }
        )
        self.downloadingItemWidget.setFixedWidth(0)
        self.VerticalSeparator.setVisible(False)
        self.showDownloadingItemBtn.toggled.connect(self.switchDownloadingItemWidget)

    @pyqtSlot(int)
    def onPageChangedRefresh(self, currentChanged):
        if currentChanged == 3:
            self.subTitleLabel.setText(
                self.tr(
                    f"Aria2引擎高速驱动！ - 当前下载源：{settingsVariables.downloadSourceTextList[settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))]}"
                )
            )
            self.downloadStackedWidget.setCurrentWidget(
                self.dsList[settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))]
            )
            self.refreshDownloads()

    def refreshDownloads(self):
        """刷新下载页面主逻辑"""
        # FastMirror
        if self.downloadStackedWidget.currentIndex() == 0:
            if downloadVariables.FastMirrorAPIDict:
                if downloadVariables.FastMirrorAPIDict["name"] != -1:
                    self.initFastMirrorCoreListWidget()
                else:
                    self.showFastMirrorFailedTip()
            else:
                self.getFastMirrorAPI()
        # PolarsAPI
        elif self.downloadStackedWidget.currentIndex() == 2:
            if downloadVariables.PolarTypeDict:
                if downloadVariables.PolarTypeDict["name"] != -1:
                    self.initPolarsTypeListWidget()
                else:
                    self.showPolarsAPIFailedTip()
            else:
                self.getPolarsAPI()
        # Akira Cloud
        elif self.downloadStackedWidget.currentIndex() == 3:
            if downloadVariables.AkiraTypeList:
                if len(downloadVariables.AkiraTypeList):
                    self.initAkiraTypeListWidget()
                else:
                    self.showAkiraFailedTip()
            else:
                self.getAkiraInfo()
        # MCSLAPI
        elif self.downloadStackedWidget.currentIndex() == 1:
            # 如果存在列表且不为空,则不再重新获取
            if downloadVariables.MCSLAPIDownloadUrlDict:
                idx = self.MCSLAPIStackedWidget.currentIndex()
                if (
                    str(downloadVariables.MCSLAPIDownloadUrlDict[idx]["downloadFileTitles"]) != "-2"
                    or str(downloadVariables.MCSLAPIDownloadUrlDict[idx]["downloadFileTitles"])
                    != "-1"
                ):
                    self.initMCSLAPIDownloadWidget(n=idx)
                else:
                    self.showMCSLAPIFailedWidget()
            else:
                self.getMCSLAPI()
                self.refreshMCSLAPIBtn.setEnabled(False)

    ###########
    # MCSLAPI #
    ###########

    def releaseMCSLAPIMemory(self):
        for layout in self.MCSLAPILayoutList:
            layout.removeItem(self.scrollAreaSpacer)
            for i in reversed(range(layout.count())):
                try:
                    layout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    layout.itemAt(i).widget().deleteLater()
                    del layout.itemAt(i).widget
                except AttributeError:
                    pass

    def getMCSLAPI(self):
        """请求MCSLAPI"""
        workThread = self.fetchMCSLAPIDownloadURLThreadFactory.create(
            _singleton=True, finishSlot=self.updateMCSLAPIDownloadUrlDict
        )
        if workThread.isRunning():
            self.refreshMCSLAPIBtn.setEnabled(False)
            return
        else:
            self.releaseMCSLAPIMemory()
            for layout in self.MCSLAPILayoutList:
                layout.addWidget(MCSLAPILoadingWidget())
            workThread.start()
            self.refreshMCSLAPIBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updateMCSLAPIDownloadUrlDict(self, _downloadUrlDict: dict):
        """更新获取MCSLAPI结果"""
        downloadVariables.MCSLAPIDownloadUrlDict.update(_downloadUrlDict)
        idx = self.MCSLAPIStackedWidget.currentIndex()
        if (
            str(downloadVariables.MCSLAPIDownloadUrlDict[idx]["downloadFileTitles"]) != "-2"
            or str(downloadVariables.MCSLAPIDownloadUrlDict[idx]["downloadFileTitles"]) != "-1"
        ):
            self.initMCSLAPIDownloadWidget(n=idx)
        else:
            self.showMCSLAPIFailedWidget()

    def showMCSLAPIFailedWidget(self):
        layout = self.MCSLAPILayoutList[self.MCSLAPIStackedWidget.currentIndex()]
        for i2 in reversed(range(layout.count())):
            layout.itemAt(i2).widget().setParent(None)
            layout.itemAt(i2).widget().deleteLater()
            del layout.itemAt(i2).widget
        layout.addWidget(MCSLAPILoadingErrorWidget())
        self.refreshMCSLAPIBtn.setEnabled(True)

    @staticmethod
    def getMCSLAPIDownloadIcon(downloadType):
        """设置MCSLAPI源图标"""
        if downloadType == 0:
            return QPixmap(":/built-InIcons/Java.svg")
        elif downloadType == 1:
            return QPixmap(":/built-InIcons/Spigot.svg")
        elif downloadType == 2:
            return QPixmap(":/built-InIcons/Paper.png")
        elif downloadType == 3:
            return QPixmap(":/built-InIcons/Spigot.svg")
        elif downloadType == 4:
            return QPixmap(":/built-InIcons/Grass.png")
        else:
            return QPixmap(":/built-InIcons/MCSL2.png")

    def initMCSLAPIDownloadWidget(self, n: int):
        """
        初始化MCSLAPI模式下的UI\n
        n 代表第几种类型\n
        下方循环的 i 代表次数
        """
        self.releaseMCSLAPIMemory()
        self.refreshMCSLAPIBtn.setEnabled(True)
        try:
            if type(downloadVariables.MCSLAPIDownloadUrlDict[n]["downloadFileTitles"]) == list:
                for i in range(
                    len(downloadVariables.MCSLAPIDownloadUrlDict[n]["downloadFileTitles"])
                ):
                    self.tmpSingleMCSLAPIDownloadWidget = singleMCSLAPIDownloadWidget()
                    self.tmpSingleMCSLAPIDownloadWidget.MCSLAPIPixmapLabel.setPixmap(
                        self.getMCSLAPIDownloadIcon(downloadType=n)
                    )
                    self.tmpSingleMCSLAPIDownloadWidget.MCSLAPIPixmapLabel.setFixedSize(
                        QSize(60, 60)
                    )
                    self.tmpSingleMCSLAPIDownloadWidget.fileTitle.setText(
                        downloadVariables.MCSLAPIDownloadUrlDict[n]["downloadFileTitles"][i]
                    )
                    self.tmpSingleMCSLAPIDownloadWidget.fileName.setText(
                        f"{downloadVariables.MCSLAPIDownloadUrlDict[n]['downloadFileNames'][i]}.{downloadVariables.MCSLAPIDownloadUrlDict[n]['downloadFileFormats'][i]}"
                    )
                    self.tmpSingleMCSLAPIDownloadWidget.setObjectName(f"DownloadWidget{i}..{n}")
                    self.tmpSingleMCSLAPIDownloadWidget.MCSLAPIDownloadBtn.setObjectName(
                        f"DownloadBtn{i}..{n}"
                    )
                    self.tmpSingleMCSLAPIDownloadWidget.MCSLAPIDownloadBtn.clicked.connect(
                        self.downloadMCSLAPIFile
                    )
                    self.MCSLAPILayoutList[n].addWidget(self.tmpSingleMCSLAPIDownloadWidget)
                self.MCSLAPILayoutList[n].addSpacerItem(self.scrollAreaSpacer)
            else:
                self.showMCSLAPIFailedWidget()
        except TypeError:
            self.showMCSLAPIFailedWidget()

    def downloadMCSLAPIFile(self):
        """下载MCSLAPI文件"""
        if not Aria2Controller.testAria2Service():
            if not Aria2Controller.startAria2():
                box = MessageBox(
                    title=self.tr("无法下载"),
                    content=self.tr("Aria2可能未安装或启动失败。\n已尝试重新启动Aria2。"),
                    parent=self,
                )
                box.yesSignal.connect(box.deleteLater)
                box.cancelButton.setParent(None)
                box.cancelButton.deleteLater()
                del box.cancelButton
                box.exec()
                return
        sender = self.sender()
        idx = int(sender.objectName().split("..")[-1])
        idx2 = int(sender.objectName().split("..")[0].split("n")[-1])
        uri = downloadVariables.MCSLAPIDownloadUrlDict[idx]["downloadFileURLs"][idx2]
        fileName = downloadVariables.MCSLAPIDownloadUrlDict[idx]["downloadFileNames"][idx2]
        fileFormat = downloadVariables.MCSLAPIDownloadUrlDict[idx]["downloadFileFormats"][idx2]
        # 判断文件是否存在
        # TODO 完善MCSLAPI的extraData : "coreName", "MCVer", "buildVer"
        self.checkDownloadFileExists(
            fileName,
            fileFormat,
            uri,
            (fileName + "." + fileFormat, "coreName", "MCVer", "buildVer"),
        )

    ##############
    # Polars API #
    ##############

    def releasePolarsAPIMemory(self, id=0):
        layout = self.polarsTypeLayout if not id else self.polarsCoreLayout
        if layout == self.polarsCoreLayout:
            try:
                layout.removeItem(self.scrollAreaSpacer)
            except AttributeError:
                pass
        for i in reversed(range(layout.count())):
            try:
                layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
            try:
                layout.itemAt(i).widget().deleteLater()
                del layout.itemAt(i).widget
            except AttributeError:
                pass

    def getPolarsAPI(self):
        """请求Polars API"""
        workThread = self.fetchPolarsAPITypeThreadFactory.create(
            _singleton=True, finishSlot=self.updatePolarsAPIDict
        )
        if workThread.isRunning():
            self.refreshPolarsAPIBtn.setEnabled(False)
            return
        else:
            self.getPolarsStateToolTip = StateToolTip(
                self.tr("正在请求极星镜像API"), self.tr("加载中，请稍后..."), self
            )
            self.getPolarsStateToolTip.move(self.getPolarsStateToolTip.getSuitablePos())
            self.getPolarsStateToolTip.show()
            workThread.start()
            self.refreshPolarsAPIBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updatePolarsAPIDict(self, _APIDict: dict):
        """更新Polars API"""
        downloadVariables.PolarTypeDict.clear()
        downloadVariables.PolarTypeDict.update(_APIDict)
        if downloadVariables.PolarTypeDict["name"] != -1:
            self.getPolarsStateToolTip.setContent(self.tr("请求极星镜像API完毕！"))
            self.getPolarsStateToolTip.setState(True)
            self.getPolarsStateToolTip = None
            self.initPolarsTypeListWidget()
        else:
            self.getPolarsStateToolTip.setContent(self.tr("请求极星镜像API失败！"))
            self.getPolarsStateToolTip.setState(True)
            self.getPolarsStateToolTip = None
            self.showPolarsAPIFailedTip()
        self.refreshPolarsAPIBtn.setEnabled(True)

    def showPolarsAPIFailedTip(self):
        InfoBar.error(
            title=self.tr("错误"),
            content=self.tr("获取极星镜像API失败！\n尝试检查网络后，请再尝试刷新。"),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self,
        )

    def initPolarsTypeListWidget(self):
        self.releasePolarsAPIMemory()
        for i in range(len(downloadVariables.PolarTypeDict["name"])):
            self.polarsTypeLayout.addWidget(
                PolarsTypeWidget(
                    name=downloadVariables.PolarTypeDict["name"][i],
                    idx=downloadVariables.PolarTypeDict["id"][i],
                    description=downloadVariables.PolarTypeDict["description"][i],
                    slot=self.polarsTypeProcessor,
                    parent=self,
                )
            )

    def polarsTypeProcessor(self):
        self.polarsTypeLabel.setText(self.sender().property("name"))
        self.polarsDescriptionLabel.setText(self.sender().property("description"))
        self.getPolarsCoreAPI(idx=self.sender().property("id"))

    def getPolarsCoreAPI(self, idx):
        workThread = self.fetchPolarsAPICoreThreadFactory.create(
            _singleton=True, idx=idx, finishSlot=self.updatePolarsAPICoreDict
        )
        if workThread.isRunning():
            self.refreshPolarsAPIBtn.setEnabled(False)
            return
        else:
            self.getPolarsCoreStateToolTip = StateToolTip(
                self.tr("正在进一步请求极星镜像API"), self.tr("加载中，请稍后..."), self
            )
            self.getPolarsCoreStateToolTip.move(self.getPolarsCoreStateToolTip.getSuitablePos())
            self.getPolarsCoreStateToolTip.show()
            workThread.start()
            self.refreshPolarsAPIBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updatePolarsAPICoreDict(self, _APIDict: dict):
        downloadVariables.PolarCoreDict.clear()
        downloadVariables.PolarCoreDict.update(_APIDict)
        if downloadVariables.PolarCoreDict["name"] != -1:
            self.getPolarsCoreStateToolTip.setContent(self.tr("请求极星镜像API完毕！"))
            self.getPolarsCoreStateToolTip.setState(True)
            self.getPolarsCoreStateToolTip = None
            self.initPolarsCoreListWidget()
        else:
            self.getPolarsCoreStateToolTip.setContent(self.tr("请求极星镜像API失败！"))
            self.getPolarsCoreStateToolTip.setState(True)
            self.getPolarsCoreStateToolTip = None
            self.showPolarsAPIFailedTip()
        self.refreshPolarsAPIBtn.setEnabled(True)

    def initPolarsCoreListWidget(self):
        self.releasePolarsAPIMemory(1)
        for i in range(len(downloadVariables.PolarCoreDict["name"])):
            self.polarsCoreLayout.addWidget(
                FastMirrorBuildListWidget(
                    buildVer=downloadVariables.PolarCoreDict["name"][i],
                    syncTime=downloadVariables.PolarCoreDict["downloadUrl"][i],
                    coreVersion=downloadVariables.PolarCoreDict["downloadUrl"][i],
                    btnSlot=self.downloadPolarsAPIFile,
                    parent=self,
                )
            )
        self.polarsCoreLayout.addItem(self.scrollAreaSpacer)

    def downloadPolarsAPIFile(self):
        """下载极星镜像API文件"""
        if not Aria2Controller.testAria2Service():
            if not Aria2Controller.startAria2():
                box = MessageBox(
                    title=self.tr("无法下载"),
                    content=self.tr("Aria2可能未安装或启动失败。\n已尝试重新启动Aria2。"),
                    parent=self,
                )
                box.yesSignal.connect(box.deleteLater)
                box.cancelButton.setParent(None)
                box.cancelButton.deleteLater()
                del box.cancelButton
                box.exec()
                return
        uri = self.sender().property("core_version")
        fileFormat = self.sender().parent().buildVerLabel.text().split(".")[-1]
        fileName = self.sender().parent().buildVerLabel.text().replace("." + fileFormat, "")
        # 判断文件是否存在
        self.checkDownloadFileExists(
            fileName,
            fileFormat,
            uri,
            (fileName + "." + fileFormat, "coreName", "MCVer", "buildVer"),
        )

    ###############
    # Akira Cloud #
    ###############

    def releaseAkiraMemory(self, id=0):
        layout = self.akiraTypeLayout if not id else self.akiraCoreLayout
        if layout == self.akiraCoreLayout:
            try:
                layout.removeItem(self.scrollAreaSpacer)
            except AttributeError:
                pass
        for i in reversed(range(layout.count())):
            try:
                layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
            try:
                layout.itemAt(i).widget().deleteLater()
                del layout.itemAt(i).widget
            except AttributeError:
                pass

    def getAkiraInfo(self):
        """请求Polars API"""
        workThread = self.fetchAkiraTypeThreadFactory.create(
            _singleton=True, finishSlot=self.updateAkiraTypeList
        )
        if workThread.isRunning():
            self.refreshAkiraCloudBtn.setEnabled(False)
            return
        else:
            self.getAkiraStateToolTip = StateToolTip(
                self.tr("正在请求Akira Cloud镜像站"), self.tr("加载中，请稍后..."), self
            )
            self.getAkiraStateToolTip.move(self.getAkiraStateToolTip.getSuitablePos())
            self.getAkiraStateToolTip.show()
            workThread.start()
            self.refreshAkiraCloudBtn.setEnabled(False)

    @pyqtSlot(list)
    def updateAkiraTypeList(self, _APIList):
        downloadVariables.AkiraTypeList = _APIList
        if len(downloadVariables.AkiraTypeList):
            self.getAkiraStateToolTip.setContent(self.tr("请求Akira Cloud镜像站完毕！"))
            self.getAkiraStateToolTip.setState(True)
            self.getAkiraStateToolTip = None
            self.initAkiraTypeListWidget()
        else:
            self.getAkiraStateToolTip.setContent(self.tr("请求Akira Cloud镜像站失败！"))
            self.getAkiraStateToolTip.setState(True)
            self.getAkiraStateToolTip = None
            self.showAkiraFailedTip()
        self.refreshAkiraCloudBtn.setEnabled(True)

    def showAkiraFailedTip(self):
        InfoBar.error(
            title=self.tr("错误"),
            content=self.tr("获取Akira Cloud镜像站信息失败！\n尝试检查网络后，请再尝试刷新。"),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self,
        )

    def initAkiraTypeListWidget(self):
        self.releaseAkiraMemory()
        for i in range(len(downloadVariables.AkiraTypeList)):
            self.akiraTypeLayout.addWidget(
                PolarsTypeWidget(
                    name=downloadVariables.AkiraTypeList[i],
                    idx=1,
                    description="",
                    slot=self.akiraTypeProcessor,
                    parent=self,
                )
            )

    def akiraTypeProcessor(self):
        self.akiraTypeLabel.setText(self.sender().property("name"))
        self.getAkiraCore(coreType=self.sender().property("name"))

    def getAkiraCore(self, coreType):
        workThread = self.fetchAkiraCoreThreadFactory.create(
            _singleton=True, coreType=coreType, finishSlot=self.updateAkiraAPICoreDict
        )
        if workThread.isRunning():
            self.refreshAkiraCloudBtn.setEnabled(False)
            return
        else:
            self.getAkiraCoreStateToolTip = StateToolTip(
                self.tr("正在进一步请求Akira Cloud镜像站"), self.tr("加载中，请稍后..."), self
            )
            self.getAkiraCoreStateToolTip.move(self.getAkiraCoreStateToolTip.getSuitablePos())
            self.getAkiraCoreStateToolTip.show()
            workThread.start()
            self.refreshAkiraCloudBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updateAkiraAPICoreDict(self, _APIDict: dict):
        downloadVariables.AkiraCoreDict.clear()
        downloadVariables.AkiraCoreDict.update(_APIDict)
        if downloadVariables.AkiraCoreDict["name"] != "-1":
            self.getAkiraCoreStateToolTip.setContent(self.tr("请求Akira Cloud镜像站完毕！"))
            self.getAkiraCoreStateToolTip.setState(True)
            self.getAkiraCoreStateToolTip = None
            self.initAkiraCoreListWidget()
        else:
            self.getAkiraCoreStateToolTip.setContent(self.tr("请求Akira Cloud镜像站失败！"))
            self.getAkiraCoreStateToolTip.setState(True)
            self.getAkiraCoreStateToolTip = None
            self.showAkiraFailedTip()
        self.refreshAkiraCloudBtn.setEnabled(True)

    def initAkiraCoreListWidget(self):
        self.releaseAkiraMemory(1)
        for i in range(len(downloadVariables.AkiraCoreDict["list"])):
            w = FastMirrorBuildListWidget(
                buildVer=downloadVariables.AkiraCoreDict["list"][i],
                syncTime="",
                coreVersion=downloadVariables.AkiraCoreDict["name"],
                btnSlot=self.downloadAkiraFile,
                parent=self,
            )
            w.syncTimeLabel.setParent(None)
            self.akiraCoreLayout.addWidget(w)
        self.akiraCoreLayout.addItem(self.scrollAreaSpacer)

    def downloadAkiraFile(self):
        """下载Akira Cloud镜像站文件"""
        if not Aria2Controller.testAria2Service():
            if not Aria2Controller.startAria2():
                box = MessageBox(
                    title=self.tr("无法下载"),
                    content=self.tr("Aria2可能未安装或启动失败。\n已尝试重新启动Aria2。"),
                    parent=self,
                )
                box.yesSignal.connect(box.deleteLater)
                box.cancelButton.setParent(None)
                box.cancelButton.deleteLater()
                del box.cancelButton
                box.exec()
                return
        uri = f"https://mirror.akiracloud.net/{self.sender().property('core_version')}/{self.sender().parent().buildVerLabel.text()}"
        fileFormat = self.sender().parent().buildVerLabel.text().split(".")[-1]
        fileName = self.sender().parent().buildVerLabel.text().replace("." + fileFormat, "")
        # 判断文件是否存在
        self.checkDownloadFileExists(
            fileName,
            fileFormat,
            uri,
            (fileName + "." + fileFormat, "coreName", "MCVer", "buildVer"),
        )

    ##################
    # FastMirror API #
    ##################

    def releaseFMMemory(self, id=0):
        if not id:
            self.coreListLayout.removeItem(self.scrollAreaSpacer)
            for i in reversed(range(self.coreListLayout.count())):
                try:
                    self.coreListLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.coreListLayout.itemAt(i).widget().deleteLater()
                    del self.coreListLayout.itemAt(i).widget
                except AttributeError:
                    pass
        elif id == 1:
            self.versionLayout.removeItem(self.scrollAreaSpacer)
            for i in reversed(range(self.versionLayout.count())):
                try:
                    self.versionLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.versionLayout.itemAt(i).widget().deleteLater()
                    del self.versionLayout.itemAt(i).widget
                except AttributeError:
                    pass
        elif id == 2:
            self.buildLayout.removeItem(self.scrollAreaSpacer)
            for i in reversed(range(self.buildLayout.count())):
                try:
                    self.buildLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.buildLayout.itemAt(i).widget().deleteLater()
                    del self.buildLayout.itemAt(i).widget
                except AttributeError:
                    pass
        else:
            pass

    def getFastMirrorAPI(self):
        """请求FastMirror API"""
        self.releasePolarsAPIMemory()
        self.releasePolarsAPIMemory(1)
        workThread = self.fetchFastMirrorAPIThreadFactory.create(
            _singleton=True, finishSlot=self.updateFastMirrorAPIDict
        )
        if workThread.isRunning():
            self.refreshFastMirrorAPIBtn.setEnabled(False)
            return
        else:
            self.getFastMirrorStateToolTip = StateToolTip(
                self.tr("正在请求FastMirror API"), self.tr("加载中，请稍后..."), self
            )
            self.getFastMirrorStateToolTip.move(self.getFastMirrorStateToolTip.getSuitablePos())
            self.getFastMirrorStateToolTip.show()
            workThread.start()
            self.refreshFastMirrorAPIBtn.setEnabled(False)

    def getFastMirrorAPICoreVersion(self, name, mcVersion):
        """请求FastMirror API 核心的版本"""
        workThread = self.fetchFastMirrorAPICoreVersionThreadFactory.create(
            name=name,
            mcVersion=mcVersion,
            _singleton=True,
            finishSlot=self.updateFastMirrorAPICoreVersionDict,
        )
        if workThread.isRunning():
            return
        else:
            self.getFastMirrorStateToolTip = StateToolTip(
                self.tr("正在进一步请求FastMirror API"), self.tr("加载中，请稍后..."), self
            )
            self.getFastMirrorStateToolTip.move(self.getFastMirrorStateToolTip.getSuitablePos())
            self.getFastMirrorStateToolTip.show()
            workThread.start()

    @pyqtSlot(dict)
    def updateFastMirrorAPIDict(self, _APIDict: dict):
        """更新获取FastMirrorAPI结果"""
        downloadVariables.FastMirrorAPIDict.clear()
        downloadVariables.FastMirrorAPIDict.update(_APIDict)
        if downloadVariables.FastMirrorAPIDict["name"] != -1:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求FastMirror API完毕！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None
            self.initFastMirrorCoreListWidget()
        else:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求FastMirror API失败！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None
            self.showFastMirrorFailedTip()
        self.refreshFastMirrorAPIBtn.setEnabled(True)

    @pyqtSlot(dict)
    def updateFastMirrorAPICoreVersionDict(self, _APICoreVersionDict: dict):
        """更新获取FastMirrorAPI结果"""
        downloadVariables.FastMirrorAPICoreVersionDict.clear()
        downloadVariables.FastMirrorAPICoreVersionDict.update(_APICoreVersionDict)
        if downloadVariables.FastMirrorAPICoreVersionDict["name"] != -1:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求FastMirror API完毕！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None
            self.initFastMirrorCoreVersionListWidget()
        else:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求FastMirror API失败！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None

    def showFastMirrorFailedTip(self):
        i = InfoBar.error(
            title=self.tr("错误"),
            content=self.tr(
                "获取FastMirror API失败！\n尝试检查网络后，请再尝试刷新。\n或者，点击旁边的按钮看看你是不是暂时达到请求限制了。"
            ),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self,
        )
        errTestBtn = HyperlinkButton("https://download.fastmirror.net/api/v3", "测试", i, FIF.LINK)
        i.addWidget(errTestBtn)

    def initFastMirrorCoreListWidget(self):
        """FastMirror核心列表"""
        self.releaseFMMemory()
        self.releaseFMMemory(1)
        self.releaseFMMemory(2)
        for i in range(len(downloadVariables.FastMirrorAPIDict["name"])):
            self.coreListLayout.addWidget(
                FastMirrorCoreListWidget(
                    tag=downloadVariables.FastMirrorReplaceTagDict[
                        downloadVariables.FastMirrorAPIDict["tag"][i]
                    ],
                    name=downloadVariables.FastMirrorAPIDict["name"][i],
                    slot=self.fastMirrorCoreNameProcessor,
                    parent=self,
                )
            )
        self.coreListLayout.addSpacerItem(self.scrollAreaSpacer)

    def fastMirrorCoreNameProcessor(self):
        downloadVariables.selectedName = self.sender().property("name")
        self.initFastMirrorMCVersionsListWidget()
        try:
            self.buildLayout.removeItem(self.scrollAreaSpacer)
        except AttributeError:
            pass
        try:
            for i in reversed(range(self.buildLayout.count())):
                self.buildLayout.itemAt(i).widget().setParent(None)
                self.buildLayout.itemAt(i).widget().deleteLater()
                del self.buildLayout.itemAt(i).widget
        except AttributeError:
            pass

    def initFastMirrorMCVersionsListWidget(self):
        self.releaseFMMemory(1)
        self.releaseFMMemory(2)
        MCVersionList = downloadVariables.FastMirrorAPIDict["mc_versions"][
            list(downloadVariables.FastMirrorAPIDict["name"]).index(downloadVariables.selectedName)
        ]
        for i in range(len(MCVersionList)):
            MCVersion = MCVersionList[i]
            self.versionLayout.addWidget(
                FastMirrorVersionListWidget(
                    version=MCVersion,
                    slot=self.fastMirrorMCVersionProcessor,
                    parent=self,
                )
            )
        self.versionLayout.addSpacerItem(self.scrollAreaSpacer)

    def fastMirrorMCVersionProcessor(self):
        downloadVariables.selectedMCVersion = self.sender().property("version")
        self.getFastMirrorAPICoreVersion(
            name=downloadVariables.selectedName,
            mcVersion=downloadVariables.selectedMCVersion,
        )

    def initFastMirrorCoreVersionListWidget(self):
        self.releaseFMMemory(2)
        for i in range(len(downloadVariables.FastMirrorAPICoreVersionDict["name"])):
            self.buildLayout.addWidget(
                FastMirrorBuildListWidget(
                    buildVer=downloadVariables.FastMirrorAPICoreVersionDict["core_version"][i],
                    syncTime=downloadVariables.FastMirrorAPICoreVersionDict["update_time"][
                        i
                    ].replace("T", " "),
                    coreVersion=downloadVariables.FastMirrorAPICoreVersionDict["core_version"][i],
                    btnSlot=self.downloadFastMirrorAPIFile,
                    parent=self,
                )
            )
        self.buildLayout.addSpacerItem(self.scrollAreaSpacer)

    def downloadFastMirrorAPIFile(self):
        """下载FastMirror API文件"""
        if not Aria2Controller.testAria2Service():
            if not Aria2Controller.startAria2():
                box = MessageBox(
                    title=self.tr("无法下载"),
                    content=self.tr("Aria2可能未安装或启动失败。\n已尝试重新启动Aria2。"),
                    parent=self,
                )
                box.yesSignal.connect(box.deleteLater)
                box.cancelButton.setParent(None)
                box.cancelButton.deleteLater()
                del box.cancelButton
                box.exec()
                return
        buildVer = self.sender().property("core_version")
        fileName = (
            f"{downloadVariables.selectedName}-{downloadVariables.selectedMCVersion}-{buildVer}"
        )
        fileFormat = "jar"
        uri = f"https://download.fastmirror.net/download/{downloadVariables.selectedName}/{downloadVariables.selectedMCVersion}/{buildVer}"
        # 判断文件是否存在
        self.checkDownloadFileExists(
            fileName,
            fileFormat,
            uri,
            (
                f"{fileName}.jar",
                downloadVariables.selectedName,
                downloadVariables.selectedMCVersion,
                buildVer,
            ),
        )

    def checkDownloadFileExists(self, fileName, fileFormat, uri, extraData: tuple) -> bool:
        if osp.exists(
            osp.join("MCSL2", "Downloads", f"{fileName}.{fileFormat}")
        ) and not osp.exists(osp.join("MCSL2", "Downloads", f"{fileName}.{fileFormat}.aria2")):
            if cfg.get(cfg.saveSameFileException) == "ask":
                w = MessageBox(self.tr("提示"), self.tr("您要下载的文件已存在。请选择操作。"), self)
                w.yesButton.setText(self.tr("停止下载"))
                w.cancelButton.setText(self.tr("覆盖文件"))
                w.cancelSignal.connect(lambda: remove(f"MCSL2/Downloads/{fileName}.{fileFormat}"))
                w.cancelSignal.connect(
                    lambda: self.downloadFile(fileName, fileFormat, uri, extraData)
                )
                w.exec()
            elif cfg.get(cfg.saveSameFileException) == "overwrite":
                InfoBar.warning(
                    title=self.tr("警告"),
                    content=self.tr(
                        "MCSL2/Downloads文件夹存在同名文件。\n根据设置，已删除原文件并继续下载。"
                    ),
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=2222,
                    parent=self,
                )
                remove(f"MCSL2/Downloads/{fileName}.{fileFormat}")
                self.downloadFile(fileName, fileFormat, uri, extraData)
            elif cfg.get(cfg.saveSameFileException) == "stop":
                InfoBar.warning(
                    title=self.tr("警告"),
                    content=self.tr("MCSL2/Downloads文件夹存在同名文件。\n根据设置，已停止下载。"),
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=2222,
                    parent=self,
                )
        else:
            self.downloadFile(fileName, fileFormat, uri, extraData)

    def downloadFile(self, fileName, fileFormat, uri, extraData: tuple):
        downloadingInfoWidget = DownloadCard(
            fileName=f"{fileName}.{fileFormat}", url=uri, parent=self
        )
        gid = Aria2Controller.download(
            uri=uri,
            watch=True,
            info_get=downloadingInfoWidget.onInfoGet,
            stopped=downloadingInfoWidget.onDownloadFinished,
            interval=0.2,
            extraData=extraData,
        )
        downloadingInfoWidget.canceled.connect(lambda: Aria2Controller.cancelDownloadTask(gid))
        downloadingInfoWidget.paused.connect(
            lambda x: Aria2Controller.pauseDownloadTask(gid)
            if x
            else Aria2Controller.resumeDownloadTask(gid)
        )
        self.downloadingItemLayout.addWidget(downloadingInfoWidget)

    def switchDownloadingItemWidget(self):
        if self.showDownloadingItemBtn.isChecked():
            self.downloadingItemWidget.setFixedWidth(310)
            self.VerticalSeparator.setVisible(True)
            self.showDownloadingItemBtn.setText(self.tr("收起下载中列表"))
        else:
            self.downloadingItemWidget.setFixedWidth(0)
            self.VerticalSeparator.setVisible(False)
            self.showDownloadingItemBtn.setText(self.tr("展开下载中列表"))
