// BASEMAP: trench
// Camera drifts over the deep water east of Samar; SOMEWHERE OFF SAMAR on 'Samar'; depth labels 4,000 M / 6,000 M fade in on the isobaths.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const W = P("WRECK");
// isobaths from the same terrain tiles as the basemap (map px): -4000 m and -6000 m
const ISO4 = [[909,40],[922,80],[918,120],[932,160],[915,200],[939,240],[1003,280],[998,320],[994,360],[1026,400],[1044,440],[1056,480],[1087,520],[1125,560],[1146,600],[1164,640],[1181,680],[1189,720],[1188,760],[1202,800],[1207,840],[1205,880],[1207,920],[1224,960],[1240,1000],[1247,1040],[1259,1080],[1267,1120],[1279,1160],[1275,1200],[1285,1240],[1274,1280],[1324,1320],[1332,1360],[1353,1400],[1369,1440]];
const ISO6 = [[952,40],[959,80],[969,120],[986,160],[1008,200],[1039,240],[1041,280],[1047,320],[1052,360],[1086,400],[1119,440],[1133,480],[1158,520],[1181,560],[1203,600],[1219,640],[1236,680],[1246,720],[1255,760],[1254,800],[1251,840],[1266,880],[1273,920],[1283,960],[1287,1000],[1296,1040],[1303,1080],[1296,1120],[1343,1160],[1353,1200],[1353,1240],[1339,1280],[1368,1320],[1394,1360],[1409,1400]];
S.camera([[0, 1330, 690, 1.25], [END, 1420, 800, 1.45]]);
S.label("SOMEWHERE OFF SAMAR", [1560, 700], { t: wt("Samar", 0.78), anchor: "c", size: 64, gap: 0, color: WH });
S.route(ISO4, { t: 1.0, dur: 1.2, width: 4, color: ST, dash: [16, 12], ease: "power1.inOut" });
S.route(ISO6, { t: 1.4, dur: 1.2, width: 4, color: WH, dash: [16, 12], ease: "power1.inOut" });
S.label("4,000 M", [1206, 900], { t: wt("some", 1.86), anchor: "l", size: 48, gap: 24, box: true, color: ST });
S.label("6,000 M", [1262, 900], { t: wt("deepest", 2.3), anchor: "r", size: 48, gap: 24, box: true, boxColor: REDBOX });
S.finish();
