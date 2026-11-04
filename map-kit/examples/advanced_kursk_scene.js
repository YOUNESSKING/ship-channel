// MOVE 2 (move2-1 .. move2-10): the northern face of Kursk, 4-12 July 1943. Basemap kursk_hd_ref (z9, HD, dark reference grade).
// Wide shots = option 1 (multiply territory overlay kursk_ctl_<date>_mx + two-colour front), close-up battle = option 2 (glowing
// two-colour front lines only). Fronts per date: tools/make_kursk_control.py + research/FACT_NOTES_kursk.md. Positions: lat/lon -> G().
// Soviets = blue (carth, hero), Germans = red (rome).
const KD = {"north":[[1367.6,-99.4],[1369.4,-93.2],[1373.1,-80.9],[1378.5,-62.5],[1385.8,-37.8],[1393.1,-14.8],[1400.4,6.8],[1407.7,26.7],[1415.0,45.2],[1423.6,63.6],[1433.6,82.0],[1445.0,100.4],[1457.7,118.7],[1473.6,137.1],[1492.7,155.4],[1515.0,173.8],[1540.5,192.0],[1562.4,211.5],[1580.6,232.0],[1595.2,253.7],[1606.1,276.6],[1617.7,299.7],[1630.0,323.3],[1643.0,347.2],[1656.6,371.4],[1665.3,396.0],[1668.9,421.0],[1667.5,446.3],[1661.2,472.0],[1652.3,497.6],[1640.9,523.3],[1627.0,548.9],[1610.7,574.4],[1595.0,599.6],[1579.9,624.4],[1565.6,648.8],[1551.9,672.7],[1539.4,693.3],[1528.0,710.6],[1517.8,724.4],[1508.6,734.9],[1501.8,742.7],[1497.3,748.0],[1495.0,750.6],[1495.0,750.6],[1495.0,750.6],[1495.0,750.6],[1495.0,750.6]],"south":[[1251.1,780.4],[1251.1,780.4],[1251.1,780.4],[1251.1,780.4],[1251.1,780.4],[1245.9,781.1],[1235.4,782.6],[1219.7,784.9],[1198.8,787.9],[1176.3,790.1],[1152.1,791.6],[1126.4,792.4],[1099.1,792.4],[1070.6,795.4],[1041.0,801.3],[1010.3,810.2],[978.5,822.2],[948.2,835.5],[919.6,850.4],[892.5,866.8],[867.0,884.6],[846.3,906.5],[830.4,932.5],[819.2,962.5],[812.9,996.5],[813.3,1031.3],[820.6,1066.7],[834.7,1102.8],[855.6,1139.7],[875.2,1176.4],[893.4,1213.1],[910.2,1249.8],[925.7,1286.4],[939.6,1323.0],[951.9,1359.5],[962.5,1395.9],[971.6,1432.4],[980.1,1472.3],[987.8,1515.9],[994.9,1563.0],[1001.2,1613.6],[1006.0,1651.6],[1009.2,1676.9],[1010.8,1689.6]],"sector":{"jul4":[[1586.1,612.8],[1581.7,620.5],[1577.3,628.2],[1572.9,635.9],[1568.5,643.6],[1564.2,651.3],[1559.8,659.0],[1555.3,666.7],[1550.9,674.4],[1546.3,681.9],[1541.7,689.5],[1537.0,697.0],[1532.1,704.4],[1527.1,711.8],[1521.9,718.9],[1516.5,725.9],[1510.6,732.6],[1504.7,739.2],[1498.8,745.8],[1492.7,752.3],[1486.5,758.6],[1480.0,764.6],[1472.7,769.6],[1464.6,773.2],[1456.1,775.6],[1447.4,777.3],[1438.6,778.3],[1429.8,779.1],[1420.9,779.7],[1412.1,780.1],[1403.2,780.4],[1394.4,780.4],[1385.5,780.4],[1376.6,780.4],[1367.8,780.4],[1358.9,780.4],[1350.0,780.4],[1341.2,780.4],[1332.3,780.4],[1323.5,780.4],[1314.6,780.4],[1305.7,780.4],[1296.9,780.4],[1288.0,780.4],[1279.1,780.4],[1270.3,780.6],[1261.4,780.9],[1252.6,781.5],[1243.7,782.2],[1234.9,783.1],[1226.1,784.1],[1217.3,785.2],[1208.5,786.5],[1199.8,787.8],[1190.9,788.7],[1182.1,789.5],[1173.3,790.3],[1164.4,790.8],[1155.6,791.4],[1146.7,791.8],[1137.9,792.0],[1129.0,792.3],[1120.2,792.4],[1111.3,792.4],[1102.4,792.4],[1093.6,792.4],[1084.7,792.4],[1075.8,792.4],[1067.0,792.4],[1058.1,792.4]],"jul7":[[1586.1,612.8],[1581.4,621.1],[1576.7,629.3],[1572.0,637.6],[1567.3,645.9],[1562.6,654.1],[1557.8,662.4],[1553.1,670.6],[1548.2,678.8],[1543.3,686.9],[1538.3,695.0],[1533.1,702.9],[1527.8,710.9],[1522.1,718.5],[1516.4,726.0],[1510.1,733.2],[1504.0,740.5],[1498.1,748.0],[1492.5,755.6],[1487.1,763.5],[1482.1,771.6],[1476.9,779.5],[1471.6,787.4],[1466.2,795.2],[1460.7,803.0],[1455.0,810.6],[1448.8,817.8],[1441.1,823.1],[1431.7,824.1],[1422.2,823.3],[1412.8,824.0],[1403.6,826.5],[1395.1,830.7],[1386.3,834.2],[1377.1,836.6],[1367.7,837.8],[1358.3,836.6],[1349.4,833.3],[1341.3,828.4],[1333.3,823.3],[1325.2,818.2],[1317.2,813.0],[1309.3,807.8],[1301.1,803.0],[1292.7,798.4],[1284.2,794.2],[1275.5,790.4],[1266.7,786.9],[1257.3,785.1],[1247.9,784.2],[1238.4,783.8],[1228.9,784.4],[1219.4,784.9],[1210.0,786.3],[1200.6,787.6],[1191.1,788.7],[1181.6,789.6],[1172.2,790.4],[1162.7,790.9],[1153.2,791.5],[1143.7,791.9],[1134.2,792.2],[1124.7,792.4],[1115.2,792.4],[1105.7,792.4],[1096.1,792.4],[1086.6,792.4],[1077.1,792.4],[1067.6,792.4],[1058.1,792.4]],"jul11":[[1586.1,612.8],[1581.2,621.4],[1576.3,629.9],[1571.4,638.5],[1566.6,647.1],[1561.7,655.7],[1556.8,664.2],[1551.8,672.8],[1546.7,681.2],[1541.6,689.7],[1536.3,698.0],[1530.9,706.2],[1525.3,714.3],[1519.4,722.3],[1513.1,729.8],[1506.6,737.3],[1500.4,745.0],[1494.5,752.8],[1488.8,760.9],[1483.6,769.3],[1478.4,777.7],[1473.3,786.2],[1468.2,794.6],[1463.0,803.0],[1457.7,811.3],[1452.1,819.4],[1445.6,826.8],[1437.2,831.8],[1428.0,835.4],[1418.7,838.8],[1409.5,842.3],[1400.3,845.9],[1390.9,848.9],[1381.2,850.6],[1371.5,852.4],[1361.9,854.8],[1352.4,857.5],[1342.8,859.4],[1333.0,859.0],[1323.8,855.4],[1315.9,849.6],[1308.8,842.8],[1302.4,835.3],[1296.4,827.4],[1290.8,819.3],[1284.7,811.6],[1278.2,804.2],[1271.2,797.2],[1263.7,790.8],[1254.8,786.8],[1245.1,784.9],[1235.3,784.2],[1225.5,784.6],[1215.6,785.5],[1205.9,786.9],[1196.1,788.2],[1186.3,789.1],[1176.5,790.1],[1166.6,790.7],[1156.8,791.3],[1146.9,791.8],[1137.0,792.1],[1127.2,792.4],[1117.3,792.4],[1107.4,792.4],[1097.6,792.4],[1087.7,792.4],[1077.8,792.4],[1068.0,792.4],[1058.1,792.4]]},"rail":[[1338.5,389.7],[1338.8,390.5],[1339.3,392.1],[1340.2,394.4],[1341.3,397.5],[1342.7,401.5],[1344.3,406.2],[1346.3,411.7],[1348.5,417.9],[1351.0,424.5],[1353.9,431.4],[1357.0,438.7],[1360.4,446.2],[1364.1,454.1],[1368.1,462.3],[1372.4,470.8],[1377.0,479.6],[1382.1,489.1],[1387.7,499.3],[1393.8,510.2],[1400.5,521.7],[1407.6,534.0],[1415.2,546.9],[1423.4,560.5],[1432.0,574.8],[1439.4,588.8],[1445.4,602.5],[1450.2,616.0],[1453.6,629.2],[1455.8,642.1],[1456.7,654.7],[1456.2,667.0],[1454.5,679.1],[1453.0,690.4],[1451.8,700.9],[1450.8,710.6],[1450.2,719.6],[1449.7,727.8],[1449.6,735.3],[1449.7,742.0],[1450.0,747.9],[1450.2,754.0],[1450.1,760.3],[1449.9,766.8],[1449.4,773.5],[1448.8,780.4],[1447.9,787.5],[1446.9,794.8],[1445.6,802.4],[1444.8,810.1],[1444.6,817.9],[1444.8,825.9],[1445.4,834.1],[1446.6,842.5],[1448.3,851.0],[1450.4,859.7],[1453.1,868.5],[1455.6,877.4],[1458.0,886.2],[1460.4,895.1],[1462.6,904.0],[1464.7,912.9],[1466.7,921.8],[1468.6,930.6],[1470.5,939.5],[1471.6,948.8],[1472.0,958.4],[1471.8,968.4],[1470.9,978.8],[1469.3,989.5],[1467.0,1000.6],[1464.1,1012.1],[1460.4,1023.9],[1456.5,1036.0],[1452.3,1048.4],[1447.8,1061.0],[1443.0,1073.9],[1438.0,1087.1],[1432.6,1100.6],[1427.0,1114.3],[1421.1,1128.3],[1415.4,1141.7],[1409.9,1154.6],[1404.7,1167.0],[1399.7,1178.7],[1394.9,1189.9],[1390.4,1200.6],[1386.0,1210.7],[1382.0,1220.2],[1378.4,1228.6],[1375.3,1235.7],[1372.7,1241.7],[1370.7,1246.4],[1369.1,1250.0],[1368.1,1252.4],[1367.6,1253.6]],"wide":{"jul4":[[1367.6,-99.4],[1369.4,-93.2],[1373.1,-80.9],[1378.5,-62.5],[1385.8,-37.8],[1393.1,-14.8],[1400.4,6.8],[1407.7,26.7],[1415.0,45.2],[1423.6,63.6],[1433.6,82.0],[1445.0,100.4],[1457.7,118.7],[1473.6,137.1],[1492.7,155.4],[1515.0,173.8],[1540.5,192.0],[1562.4,211.5],[1580.6,232.0],[1595.2,253.7],[1606.1,276.6],[1617.7,299.7],[1630.0,323.3],[1643.0,347.2],[1656.6,371.4],[1665.3,396.0],[1668.9,421.0],[1667.5,446.3],[1661.2,472.0],[1652.3,497.6],[1640.9,523.3],[1627.0,548.9],[1610.7,574.4],[1595.0,599.6],[1579.9,624.4],[1565.6,648.8],[1551.9,672.7],[1539.4,693.3],[1528.0,710.6],[1517.8,724.4],[1508.6,734.9],[1500.2,744.2],[1492.5,752.5],[1485.5,759.6],[1479.1,765.5],[1471.4,770.4],[1462.3,774.1],[1451.8,776.7],[1440.0,778.2],[1427.7,779.3],[1414.9,780.0],[1401.7,780.4],[1388.1,780.4],[1374.4,780.4],[1360.8,780.4],[1347.1,780.4],[1333.5,780.4],[1319.4,780.4],[1304.8,780.4],[1289.8,780.4],[1274.3,780.4],[1257.5,781.1],[1239.3,782.6],[1219.7,784.9],[1198.8,787.9],[1176.3,790.1],[1152.1,791.6],[1126.4,792.4],[1099.1,792.4],[1070.6,795.4],[1041.0,801.3],[1010.3,810.2],[978.5,822.2],[948.2,835.5],[919.6,850.4],[892.5,866.8],[867.0,884.6],[846.3,906.5],[830.4,932.5],[819.2,962.5],[812.9,996.5],[813.3,1031.3],[820.6,1066.7],[834.7,1102.8],[855.6,1139.7],[875.2,1176.4],[893.4,1213.1],[910.2,1249.8],[925.7,1286.4],[939.6,1323.0],[951.9,1359.5],[962.5,1395.9],[971.6,1432.4],[980.1,1472.3],[987.8,1515.9],[994.9,1563.0],[1001.2,1613.6],[1006.0,1651.6],[1009.2,1676.9],[1010.8,1689.6]],"jul7":[[1367.6,-99.4],[1369.4,-93.2],[1373.1,-80.9],[1378.5,-62.5],[1385.8,-37.8],[1393.1,-14.8],[1400.4,6.8],[1407.7,26.7],[1415.0,45.2],[1423.6,63.6],[1433.6,82.0],[1445.0,100.4],[1457.7,118.7],[1473.6,137.1],[1492.7,155.4],[1515.0,173.8],[1540.5,192.0],[1562.4,211.5],[1580.6,232.0],[1595.2,253.7],[1606.1,276.6],[1617.7,299.7],[1630.0,323.3],[1643.0,347.2],[1656.6,371.4],[1665.3,396.0],[1668.9,421.0],[1667.5,446.3],[1661.2,472.0],[1652.3,497.6],[1640.9,523.3],[1627.0,548.9],[1610.7,574.4],[1595.0,599.6],[1579.9,624.4],[1565.6,648.8],[1551.9,672.7],[1539.4,693.3],[1528.0,710.6],[1517.8,724.4],[1508.6,734.9],[1500.7,744.6],[1493.9,753.6],[1488.2,761.8],[1483.6,769.2],[1478.6,777.0],[1473.2,785.2],[1467.2,793.8],[1460.9,802.8],[1455.4,810.1],[1450.8,815.7],[1447.2,819.6],[1444.5,821.8],[1440.6,823.3],[1435.6,824.1],[1429.5,824.1],[1422.2,823.3],[1415.4,823.5],[1409.0,824.6],[1403.1,826.7],[1397.7,829.6],[1391.8,832.2],[1385.4,834.5],[1378.6,836.3],[1371.2,837.8],[1364.0,837.8],[1356.7,836.3],[1349.4,833.3],[1342.1,828.9],[1334.4,824.0],[1326.2,818.8],[1317.5,813.2],[1308.5,807.3],[1298.9,801.7],[1288.9,796.4],[1278.4,791.6],[1267.5,787.1],[1254.1,784.5],[1238.1,783.8],[1219.7,784.9],[1198.8,787.9],[1176.3,790.1],[1152.1,791.6],[1126.4,792.4],[1099.1,792.4],[1070.6,795.4],[1041.0,801.3],[1010.3,810.2],[978.5,822.2],[948.2,835.5],[919.6,850.4],[892.5,866.8],[867.0,884.6],[846.3,906.5],[830.4,932.5],[819.2,962.5],[812.9,996.5],[813.3,1031.3],[820.6,1066.7],[834.7,1102.8],[855.6,1139.7],[875.2,1176.4],[893.4,1213.1],[910.2,1249.8],[925.7,1286.4],[939.6,1323.0],[951.9,1359.5],[962.5,1395.9],[971.6,1432.4],[980.1,1472.3],[987.8,1515.9],[994.9,1563.0],[1001.2,1613.6],[1006.0,1651.6],[1009.2,1676.9],[1010.8,1689.6]],"jul11":[[1367.6,-99.4],[1369.4,-93.2],[1373.1,-80.9],[1378.5,-62.5],[1385.8,-37.8],[1393.1,-14.8],[1400.4,6.8],[1407.7,26.7],[1415.0,45.2],[1423.6,63.6],[1433.6,82.0],[1445.0,100.4],[1457.7,118.7],[1473.6,137.1],[1492.7,155.4],[1515.0,173.8],[1540.5,192.0],[1562.4,211.5],[1580.6,232.0],[1595.2,253.7],[1606.1,276.6],[1617.7,299.7],[1630.0,323.3],[1643.0,347.2],[1656.6,371.4],[1665.3,396.0],[1668.9,421.0],[1667.5,446.3],[1661.2,472.0],[1652.3,497.6],[1640.9,523.3],[1627.0,548.9],[1610.7,574.4],[1595.0,599.6],[1579.9,624.4],[1565.6,648.8],[1551.9,672.7],[1539.4,693.3],[1528.0,710.6],[1517.8,724.4],[1508.6,734.9],[1500.7,744.6],[1493.9,753.6],[1488.2,761.8],[1483.6,769.2],[1478.6,777.4],[1473.2,786.4],[1467.2,796.1],[1460.9,806.5],[1455.4,814.9],[1450.8,821.3],[1447.2,825.5],[1444.5,827.8],[1440.9,830.0],[1436.3,832.2],[1430.8,834.4],[1424.5,836.7],[1418.3,838.9],[1412.4,841.1],[1406.7,843.4],[1401.3,845.6],[1395.8,847.5],[1390.4,849.0],[1384.9,850.1],[1379.4,850.9],[1373.0,852.1],[1365.7,853.8],[1357.5,856.0],[1348.5,858.7],[1340.0,859.7],[1332.3,858.9],[1325.3,856.4],[1318.9,852.3],[1312.3,846.5],[1305.5,839.2],[1298.5,830.4],[1291.2,819.9],[1283.9,810.6],[1276.6,802.4],[1269.3,795.3],[1262.0,789.4],[1251.3,785.6],[1237.2,784.1],[1219.7,784.9],[1198.8,787.9],[1176.3,790.1],[1152.1,791.6],[1126.4,792.4],[1099.1,792.4],[1070.6,795.4],[1041.0,801.3],[1010.3,810.2],[978.5,822.2],[948.2,835.5],[919.6,850.4],[892.5,866.8],[867.0,884.6],[846.3,906.5],[830.4,932.5],[819.2,962.5],[812.9,996.5],[813.3,1031.3],[820.6,1066.7],[834.7,1102.8],[855.6,1139.7],[875.2,1176.4],[893.4,1213.1],[910.2,1249.8],[925.7,1286.4],[939.6,1323.0],[951.9,1359.5],[962.5,1395.9],[971.6,1432.4],[980.1,1472.3],[987.8,1515.9],[994.9,1563.0],[1001.2,1613.6],[1006.0,1651.6],[1009.2,1676.9],[1010.8,1689.6]]},"rivers":[]};
const B = Battle();
const { at, P: PS } = B;
const END = B.T.duration;
const K = FXK(B);
const GG = GGK(B);
const G = GG.proj(9, 77312, 42277);
const p = (n) => "move2-" + n;
const SFLAG = "assets/media/ussr_flag.png", GFLAG = "assets/media/ger_reich_flag.png";

// ---------- beats (spoken words) ----------
const T_SUMMER = at(p(1), "By the summer"), T_BULGE = at(p(1), "huge bulge"), T_CENTRAL = at(p(1), "Central Front"), T_700 = at(p(1), "more than seven hundred"),
  T_NORTH = at(p(1), "Facing him"), T_MODEL = at(p(1), "Walther Model"), T_335 = at(p(1), "about three hundred and thirty-five"), T_TIGERS = at(p(1), "new Tigers"),
  T_FERD = at(p(1), "Ferdinand");
const S2 = PS(p(2)), T_CITADEL = at(p(2), "Operation Citadel"), T_STRIKE_S = at(p(2), "strike south"), T_ANOTHER = at(p(2), "another German army"),
  T_MEET = at(p(2), "meet at Kursk"), T_TRAP = at(p(2), "trapping everything"), T_BELIEVED = at(p(2), "Model believed");
const S3 = PS(p(3)), T_300 = at(p(3), "almost three hundred"), T_GUESS = at(p(3), "guess where"), T_RAIL = at(p(3), "the railway that ran"),
  T_PONYRI = at(p(3), "towards Ponyri"), T_RISK = at(p(3), "huge risk"), T_PACKED = at(p(3), "He packed"), T_40 = at(p(3), "only about forty"),
  T_ARTY = at(p(3), "entire artillery corps");
const S4 = PS(p(4)), T_THREE = at(p(4), "three defensive belts"), T_MINES = at(p(4), "minefields"), T_STRONG = at(p(4), "anti-tank strongpoints"),
  T_CLUSTER = at(p(4), "each one a cluster"), T_EVEN = at(p(4), "Even if");
const S5 = PS(p(5)), T_SAPPERS = at(p(5), "captured German sappers"), T_DAWN_SAID = at(p(5), "They said"), T_ZHUKOV = at(p(5), "With Zhukov"),
  T_FIRST = at(p(5), "fire first"), T_EARLY = at(p(5), "In the early hours"), T_HUNDREDS = at(p(5), "hundreds of Soviet guns"), T_LESS = at(p(5), "less damage"),
  T_LOST = at(p(5), "lost surprise");
const S6 = PS(p(6)), T_INTO = at(p(6), "pushed into the first belt"), T_MINEF = at(p(6), "ran straight into"), T_BROKE = at(p(6), "broke into"),
  T_COST = at(p(6), "every kilometre"), T_SECOND = at(p(6), "behind the first belt");
const S7 = PS(p(7)), T_WEEK = at(p(7), "almost a week"), T_STATION = at(p(7), "railway station changed"), T_LITTLE = at(p(7), "little Stalingrad"),
  T_HEAVY = at(p(7), "German heavy armour"), T_CUTDOWN = at(p(7), "cut down by artillery"), T_GREAT = at(p(7), "The great Ferdinands"),
  T_FLANKS = at(p(7), "both flanks"), T_CLIMB = at(p(7), "climbed onto them");
const S8 = PS(p(8)), T_RESERVES = at(p(8), "threw in his reserves"), T_READY = at(p(8), "Rokossovsky was ready"), T_SHIFT = at(p(8), "shifting tanks"),
  T_WEEK2 = at(p(8), "After a week"), T_BARELY = at(p(8), "barely ten"), T_NOTEVEN = at(p(8), "not even broken");
const S9 = PS(p(9)), T_ARMIES = at(p(9), "Soviet armies attacked"), T_PULL = at(p(9), "pull his divisions back"), T_OVER = at(p(9), "Citadel was over"),
  T_LAST = at(p(9), "the last great");
const S10 = PS(p(10)), T_34 = at(p(10), "almost thirty-four"), T_15 = at(p(10), "fifteen thousand"), T_9TH = at(p(10), "The Ninth Army lost"),
  T_GONE = at(p(10), "gone for good"), T_READ = at(p(10), "had read where"), T_BEND = at(p(10), "Bend, don't break"), T_BLOW = at(p(10), "Read the blow before");

// ---------- places (map px) ----------
const OREL = G(52.967, 36.069), KURSK = G(51.730, 36.193), PON = G(52.319, 36.302), OLK = G(52.256, 36.125), TEP = G(52.273, 36.006),
  SOB = G(52.321, 36.087), MALO = G(52.400, 36.500), FAT = G(52.090, 35.860), KROMY = G(52.687, 35.790), GLAZ = G(52.499, 36.322),
  NOVOSIL = G(52.97, 37.04), BOLKHOV = G(53.44, 36.00);
const T_PUSH = T_PONYRI - 0.6;            // camera starts to push in: wide set (option 1) -> close set (option 2)
const T_SWAP = T_PONYRI + 1.6;            // wide labels/flags/overlay gone, close labels in
const T_OUT = S9 + 0.4;                   // zoom back out to the whole Orel bulge (option 1 again)

// ---------- map layers ----------
const OV4 = B.image("assets/media/kursk_ctl_jul4_mx.png", 0, 0, 2880, 1620, { t: 0, dur: 0.01, until: T_SWAP });
OV4.style.mixBlendMode = "multiply";
const OV11 = B.image("assets/media/kursk_ctl_jul11_mx.png", 0, 0, 2880, 1620, { t: T_OUT + 0.6, dur: 1.2 });
OV11.style.mixBlendMode = "multiply";
B.image("assets/media/kursk_geo_base.png", 0, 0, 2880, 1620, { t: 0, dur: 0.01 });
const TOWNS = B.image("assets/media/kursk_geo_towns.png", 0, 0, 2880, 1620, { t: 0, dur: 0.01, until: T_PUSH + 0.6 });
B.image("assets/media/kursk_geo_towns.png", 0, 0, 2880, 1620, { t: T_OUT + 1.0, dur: 1.0 });
const LV = LivingK(B);
LV.clouds({ n: 8, opacity: 0.24 });
if (KD.rivers && KD.rivers.length) LV.shimmer(KD.rivers);
LV.scaleBar(186.76); LV.north();

// ---------- camera ----------
const WIDE = [1440, 810, 0.667], CLOSE = [1405, 815, 3.2];
B.camera([[0, 1430, 800, 0.70], [S2 - 1, 1440, 820, 0.667], [S2 + 2, 1420, 900, 0.667], [S3, 1400, 860, 0.68], [T_300, 1200, 800, 0.70],
  [T_RAIL, 1390, 760, 0.95], [T_PONYRI + 1.8, 1405, 800, 2.1], [T_40, 1400, 810, 2.35], [S4 - 0.3, 1400, 815, 2.5], [S4 + 2.5, ...CLOSE],
  [T_EVEN, 1400, 822, 3.3], [S5 + 1, 1405, 790, 3.0], [T_EARLY, 1410, 780, 3.0], [T_LESS, 1405, 795, 3.1], [S6 + 1.5, 1405, 805, 3.2],
  [T_SECOND, 1410, 815, 3.3], [S7 + 1.5, 1440, 830, 3.6], [T_HEAVY, 1440, 832, 3.6], [T_GREAT, 1435, 832, 3.7], [S8 + 1.5, 1385, 855, 3.4],
  [T_SHIFT, 1360, 875, 3.0], [T_BARELY, 1380, 840, 2.9], [S9 - 0.3, 1380, 830, 2.8], [S9 + 3.5, 1160, 600, 0.95], [T_LAST, 1165, 610, 0.97],
  [S10 + 2, 1150, 620, 0.92], [END, 1150, 630, 0.9]]);
SFX("ref:riser", T_PONYRI - 2.2); SFX("ref:whoosh", T_PONYRI - 0.2); SFX("ref:whoosh", S9 + 0.2);

// ---------- dates ----------
B.showDate(0.1);
B.date("JULY 1943", 0.3, S5, 34);
B.date("4 JULY 1943", S5, T_EARLY, 34);
B.date("5 JULY · 02:20", T_EARLY, S6 - 0.4, 30);
B.date("5 JULY 1943", S6 - 0.4, S7 + 0.4, 34);
B.date("5-11 JULY 1943", S7 + 0.4, T_BARELY, 30);
B.date("11 JULY 1943", T_BARELY, S9, 34);
B.date("12 JULY 1943", S9, null, 34);

// ---------- helpers ----------
const box = (txt, x, y, t, size = 22, until, o = {}) => { if (o.pop !== false) SFX("ref:pop", t); return GG.pin(`<div style="background:#f1eee6;color:#111;font-family:Oswald;font-weight:500;letter-spacing:.3em;padding:${(size * 0.2).toFixed(1)}px ${(size * 0.35).toFixed(1)}px ${(size * 0.2).toFixed(1)}px ${(size * 0.6).toFixed(1)}px;font-size:${size}px;line-height:1.25;box-shadow:0 ${size * 0.08}px ${size * 0.3}px rgba(0,0,0,.6);white-space:nowrap">${txt}</div>`, x, y, { t, until, anchor: o.anchor }); };
const flag = (src, name, x, y, t, until, w = 170, fs = 34) => GG.pin(`<div style="display:flex;flex-direction:column;align-items:center;gap:${w * 0.04}px"><img src="${src}" style="width:${w}px;display:block;border:${Math.max(1, w * 0.015)}px solid #1a1712;box-shadow:0 ${w * 0.02}px ${w * 0.05}px rgba(0,0,0,0.55)"><div class="gg-lbl" style="position:relative;font-size:${fs}px;color:#f7f3ea;text-shadow:0 ${fs * 0.06}px ${fs * 0.12}px #000;letter-spacing:0.08em">${name}</div></div>`, x, y, { t, pop: true, until });
// counter with a period flag chip (lib FLAGS has no USSR key, so the USSR chip is added here with the same style)
const unit = (id, side, x, y, t, o = {}) => {
  B.unit({ id, side, x, y, w: o.w || 22, h: o.h || 15, t, label: o.label });
  K.counter(id, { icon: o.icon || "infantry", size: o.size, flag: side === "rome" ? "ger" : undefined });
  const u = B.units[id];
  if (side === "carth") { const img = document.createElement("img"); img.className = "fxk-flag"; img.src = SFLAG; Object.assign(img.style, { height: u.h * 0.55 + "px", left: -u.h * 0.35 + "px", top: -u.h * 0.3 + "px" }); u.el.appendChild(img); }
  if (o.label) { const tg = u.el.querySelector(".tag"); tg.style.fontSize = (o.fs || Math.max(5, u.h * 0.42)) + "px"; tg.style.padding = `0 ${u.h * 0.2}px`; tg.style.whiteSpace = "nowrap"; tg.style.marginTop = u.h * 0.08 + "px"; }
  return u;
};
const fade = (ids, t, to = 0.0, dur = 0.6) => ids.forEach((k) => B.tl.to(B.units[k].el, { autoAlpha: to, duration: dur }, t));
const badge = (o) => { const el = K.badge(o); const bg = el.querySelector('div[style*="border-radius:50%"]'); if (bg) bg.style.background = `url(${o.flagSrc}) center/cover`; return el; };
// artillery shot: gun fires (quiet), shell arc, impact carries the boom + locked shake
const shoot = (from, to, t, o = {}) => {
  K.gun(from[0], from[1], t, { unit: o.unit, dx: o.dx || 0, dy: o.dy || -2, sfx: o.sfx });
  const dur = o.dur || 1.0;
  GG.arc(from[0], from[1], to[0], to[1], t + 0.05, { dur, width: o.width || 1.2, h: o.h, impact: false, color: o.color });
  K.impact(to[0], to[1], t + 0.05 + dur, { r: o.r || 5, puffs: 2 });
};
// glowing railway (track + ties) with a gold glow
const NS = "http://www.w3.org/2000/svg", OVL = document.getElementById("overlay");
const railway = (pts, t, until) => {
  const d = "M" + pts.map((q) => q[0] + " " + q[1]).join(" L");
  const g = document.createElementNS(NS, "g");
  g.innerHTML = `<path d="${d}" fill="none" stroke="#ffd36a" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" opacity="0.55" filter="url(#k2-glow)"/>
    <path d="${d}" fill="none" stroke="#1a1712" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${d}" fill="none" stroke="#f3e6c0" stroke-width="2.6" stroke-dasharray="5 4" stroke-linejoin="round"/>`;
  if (!document.getElementById("k2-glow")) { const defs = document.createElementNS(NS, "defs"); defs.innerHTML = `<filter id="k2-glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>`; OVL.insertBefore(defs, OVL.firstChild); }
  OVL.appendChild(g); GG.hide(g);
  B.tl.to(g, { autoAlpha: 1, duration: 0.8 }, t);
  const glow = g.querySelector("path");
  B.tl.to(glow, { opacity: 0.95, duration: 0.7, yoyo: true, repeat: 5, ease: "sine.inOut" }, t + 0.8);
  if (until != null) B.tl.to(g, { autoAlpha: 0, duration: 0.8 }, until);
  return g;
};
// minefield: hatched patch (small crosses) with a dashed rim
const mines = (pts, t, until) => {
  if (!document.getElementById("k2-mines")) {
    const defs = document.createElementNS(NS, "defs");
    defs.innerHTML = `<pattern id="k2-mines" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(20)"><path d="M1 1 L3 3 M3 1 L1 3" stroke="#f2dfa0" stroke-width="0.55" opacity="0.85"/></pattern>`;
    OVL.insertBefore(defs, OVL.firstChild);
  }
  const pg = document.createElementNS(NS, "polygon");
  pg.setAttribute("points", pts.map((q) => q.join(",")).join(" ")); pg.setAttribute("fill", "url(#k2-mines)");
  pg.setAttribute("stroke", "rgba(242,223,160,0.75)"); pg.setAttribute("stroke-width", "0.7"); pg.setAttribute("stroke-dasharray", "2 2");
  OVL.appendChild(pg); GG.hide(pg); B.tl.to(pg, { autoAlpha: 1, duration: 0.8 }, t);
  if (until != null) B.tl.to(pg, { autoAlpha: 0, duration: 0.8 }, until);
  return pg;
};
// anti-tank strongpoint: blue ring with an anti-tank gun mark
const strong = (x, y, t, until) => {
  const el = GG.pin(`<svg width="13" height="13" viewBox="0 0 40 40" style="display:block;overflow:visible;filter:drop-shadow(0 1px 1px rgba(0,0,0,.7))"><circle cx="20" cy="20" r="17" fill="#1f4fc4" stroke="#f3eee2" stroke-width="4"/><path d="M9 26 L31 14" stroke="#f3eee2" stroke-width="4" stroke-linecap="round"/><circle cx="15" cy="27" r="4" fill="none" stroke="#f3eee2" stroke-width="3"/></svg>`, x, y, { t, pop: true, until });
  SFX("ref:pop", t); return el;
};
const offset = (pts, d) => pts.map((q, i) => { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1; return [+(q[0] - (dy / L) * d).toFixed(1), +(q[1] + (dx / L) * d).toFixed(1)]; });
const legend = (kind, t, until) => {
  const sw = (c) => kind === "fill" ? `<b style="display:inline-block;width:20px;height:20px;background:${c};vertical-align:-3px;margin-right:8px;border:1px solid #f7f3ea"></b>`
    : `<b style="display:inline-block;width:26px;height:6px;background:${c};box-shadow:0 0 8px ${c};vertical-align:5px;margin-right:8px"></b>`;
  const c = GG.card(`<div style="display:flex;gap:26px;font-size:22px;letter-spacing:0.08em;align-items:center">${kind === "fill" ? "" : ""}<span>${sw(kind === "fill" ? "#2e5cb2" : "#2c57b7")}SOVIET</span><span>${sw(kind === "fill" ? "#8c0c14" : "#bc2528")}GERMAN</span></div>`, "", 36, t, until);
  c.querySelector(".inner").style.cssText += "padding:12px 30px;border-top:4px solid #9fc0ea;";
  return c;
};

// ======================= move2-1: the bulge (wide, option 1) =======================
B.title("MOVE 2", "THE NORTHERN FACE OF KURSK", "JULY 1943", 0.4, T_CENTRAL - 0.4); SFX("hit", 0.5);
legend("fill", 0.6, T_SWAP);
// emblem fixed on German-held ground (the Orel bulge's west), never fades
const EM = G(52.75, 33.4);
B.image("assets/media/emblem_ger.png", EM[0] - 150, EM[1] - 150, 300, 300, { t: T_BULGE - 0.3, dur: 1.2, opacity: 0.8 }); SFX("ref:boom", T_BULGE - 0.3);
flag(GFLAG, "GERMANY", ...G(52.95, 34.6), T_BULGE + 0.4, T_SWAP);
flag(SFLAG, "USSR", ...G(51.95, 38.3), T_BULGE + 0.7, T_SWAP);
// wide fronts (option 1): the whole 4 July line, two-coloured (blue east / red west)
const FW4 = K.front({ pts: KD.wide.jul4, sideA: "carth", sideB: "rome", t: 0, dur: 1.6, width: 15, until: T_SWAP });
box("OREL", OREL[0] + 14, OREL[1] - 32, T_BULGE + 0.2, 22, T_SWAP);
box("KURSK", KURSK[0] + 4, KURSK[1] + 34, T_BULGE + 0.5, 22, T_SWAP);
box("KROMY", KROMY[0] - 6, KROMY[1] - 30, T_BULGE + 0.8, 16, T_SWAP);
box("BELGOROD ↓", 1600, 1580, T_ANOTHER, 16, T_SWAP);
B.city("", ...OREL, { r: 9, t: T_BULGE + 0.2, until: T_SWAP }); B.city("", ...KURSK, { r: 9, t: T_BULGE + 0.5, until: T_SWAP }); B.city("", ...KROMY, { r: 6, t: T_BULGE + 0.8, until: T_SWAP });
// units on screen from the first second (wide counters)
const WS = [["w48", "carth", 1615, 640, "48TH ARMY"], ["w13", "carth", 1430, 850, "13TH ARMY"], ["w70", "carth", 1235, 840, "70TH ARMY"], ["w65", "carth", 990, 900, "65TH ARMY"],
  ["w60", "carth", 1000, 1200, "60TH ARMY"]];
WS.forEach(([id, s, x, y, lab], i) => unit(id, s, x, y, 0.2 + i * 0.12, { w: 56, h: 38, label: lab, fs: 17 }));
unit("w2ta", "carth", 1330, 1010, T_CENTRAL + 0.4, { w: 56, h: 38, icon: "tank", label: "2ND TANK ARMY", fs: 17 });
const WG = [["g23", 1545, 690, "XXIII"], ["g41", 1450, 705, "XLI PZ"], ["g47", 1365, 700, "XLVII PZ"], ["g46", 1280, 715, "XLVI PZ"]];
WG.forEach(([id, x, y, lab], i) => unit(id, "rome", x, y, 0.5 + i * 0.12, { w: 56, h: 38, icon: i === 0 ? "infantry" : "tank", label: lab, fs: 17 }));
box("CENTRAL FRONT", 1700, 900, T_CENTRAL, 20, T_PUSH);
box("9TH ARMY", 1380, 600, T_NORTH, 20, T_PUSH);
box("VORONEZH FRONT", 1720, 1480, T_CENTRAL + 0.6, 16, T_SWAP);
// odds card 711,575 vs ~335,000 (counters tick up)
const odds = GG.card(`<div style="display:flex;align-items:center;gap:46px;font-weight:700;letter-spacing:0.04em"><div style="text-align:center"><div class="n1" style="font-size:70px;line-height:1;color:#6f9bff">0</div><div style="font-size:19px;letter-spacing:0.3em;color:#c9d6ff">CENTRAL FRONT</div></div><div style="font-size:30px;color:#c9b48a">VS</div><div class="c2" style="text-align:center"><div class="n2" style="font-size:70px;line-height:1;color:#ff6b6b">0</div><div style="font-size:19px;letter-spacing:0.3em;color:#ffc9c9">9TH ARMY</div></div></div>`, "gg-odds", 800, T_700 - 0.2, T_TIGERS + 0.4);
odds.querySelector(".inner").style.padding = "16px 54px 20px";
const c2 = odds.querySelector(".c2"); GG.hide(c2);
B.tl.fromTo(c2, { autoAlpha: 0, scale: 1.4 }, { autoAlpha: 1, scale: 1, duration: 0.3 }, T_335);
const countUp = (el, to, t, dur, prefix = "") => { const o = { v: 0 }; B.tl.to(o, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { el.textContent = prefix + Math.round(o.v).toLocaleString("en-US"); } }, t); for (let k = 0; k < dur / 0.12; k++) SFX("tick", t + k * 0.12); };
countUp(odds.querySelector(".n1"), 711575, T_700, 1.4); countUp(odds.querySelector(".n2"), 335000, T_335 + 0.1, 1.2, "~");
SFX("hit", T_700); SFX("hit", T_335);
badge({ name: "WALTHER MODEL", role: "9TH ARMY", photo: "assets/media/model_head.png", initials: "WM", side: "rome", corner: "br", t: T_MODEL - 0.2, until: T_FERD + 0.8, flagSrc: GFLAG });
box("TIGERS · FERDINANDS", 1450, 640, T_TIGERS, 16, S2 + 1);

// ======================= move2-2: the Citadel pincer =======================
const AN = B.arrow({ pts: [[1360, 640], [1390, 820], [1400, 980], [1400, 1120]], side: "rome", width: 26, t: T_STRIKE_S, dur: 1.8, until: S3 + 1 });
const AS = B.arrow({ pts: [[1560, 1640], [1520, 1450], [1450, 1300], [1410, 1215]], side: "rome", width: 26, t: T_ANOTHER + 0.3, dur: 1.8, until: S3 + 1 });
[AN, AS].forEach((g, i) => B.tl.to(g, { opacity: 0.62, duration: 0.5 }, (i ? T_ANOTHER + 0.3 : T_STRIKE_S) + 1.9));
SFX("ref:whoosh", T_STRIKE_S); SFX("ref:whoosh", T_ANOTHER + 0.3);
K.target(KURSK[0], KURSK[1], T_MEET, { r: 70, side: "rome", until: T_BELIEVED + 2 });
GG.stamp("CITADEL", T_CITADEL, T_MEET - 0.2, { size: 64 });
const belief = GG.card(`<div style="font-size:20px;letter-spacing:0.4em;color:#ff8a8a;text-align:center;margin-bottom:8px">MODEL BELIEVED</div><div style="font-size:50px;font-weight:700;letter-spacing:0.08em;color:#f4f1ea">"BREAK THROUGH, MEET AT KURSK"</div>`, "", 820, T_BELIEVED, S3 + 0.4);
belief.querySelector(".inner").style.borderTopColor = "#c4121f"; SFX("hit", T_BELIEVED);

// ======================= move2-3: reading the ground; the 40 km sector =======================
badge({ name: "K. ROKOSSOVSKY", role: "CENTRAL FRONT", photo: "assets/media/rokossovsky_head.png", initials: "KR", side: "carth", corner: "br", t: S3 + 0.2, until: T_GUESS + 1.5, flagSrc: SFLAG });
// his front glows (~300 km): the Central Front's part of the line, from the 48th Army's sector to the west face
const CF = KD.wide.jul4.filter((q) => q[1] > 520 && q[1] < 1380);
const cfGlow = B.highlight(CF, T_300, T_RAIL, 34); B.tl.to(cfGlow, { opacity: 0, duration: 0.8 }, T_RAIL + 0.6); SFX("ref:pop", T_300);
box("~300 KM", 700, 980, T_300 + 0.3, 26, T_RAIL + 0.5);
railway(KD.rail, T_RAIL, T_OUT);
box("OREL–KURSK RAILWAY", 1520, 520, T_RAIL + 0.4, 18, T_PONYRI);
// the bet: the 13th Army packed into ~40 km, with a whole artillery corps
const BR = [G(52.56, 35.92), G(52.57, 36.48)];
const brk = GG.pin(`<svg width="${BR[1][0] - BR[0][0] + 10}" height="18" viewBox="0 0 ${BR[1][0] - BR[0][0] + 10} 18" style="display:block;overflow:visible"><path d="M5 16 L5 4 L${BR[1][0] - BR[0][0] + 5} 4 L${BR[1][0] - BR[0][0] + 5} 16" fill="none" stroke="#1a1712" stroke-width="4"/><path d="M5 16 L5 4 L${BR[1][0] - BR[0][0] + 5} 4 L${BR[1][0] - BR[0][0] + 5} 16" fill="none" stroke="#f7f3ea" stroke-width="2"/></svg>`, (BR[0][0] + BR[1][0]) / 2, BR[0][1] - 26, { t: T_40, pop: true, until: S4 + 1.5 });
box("40 KM", (BR[0][0] + BR[1][0]) / 2, BR[0][1] - 13, T_40 + 0.1, 10, S4 + 1.5);
SFX("hit", T_40);
// close set of counters (option 2 scale): Soviet sector + flanks, German assembly areas
const CS = [["s13a", 1345, 802, "infantry"], ["s13b", 1395, 800, "infantry"], ["s13c", 1445, 806, "infantry"], ["s48", 1548, 760, "infantry"], ["s70", 1262, 800, "infantry"]];
CS.forEach(([id, x, y, ic], i) => unit(id, "carth", x, y, T_PONYRI + 0.8 + i * 0.15, { icon: ic, label: id === "s13b" ? "13TH ARMY" : id === "s48" ? "48TH" : id === "s70" ? "70TH" : undefined, fs: 5 }));
// the artillery corps and extra divisions slide in from the quiet sectors; the flanks thin out
const AR = [["a1", 1355, 902], ["a2", 1412, 904], ["a3", 1470, 884], ["a4", 1305, 898], ["a5", 1384, 928], ["a6", 1442, 926]];
AR.forEach(([id, x, y], i) => { const fx = i % 2 ? 1620 : 1170; unit(id, "carth", fx, y + 10, T_PACKED + i * 0.25, { icon: "artillery" }); B.move(id, T_PACKED + 0.3 + i * 0.25, 2.0, x, y); });
unit("s13d", "carth", 1210, 830, T_PACKED, { icon: "infantry" }); B.move("s13d", T_PACKED + 0.4, 2.0, 1420, 806);
unit("s13e", "carth", 1600, 820, T_PACKED + 0.2, { icon: "infantry" }); B.move("s13e", T_PACKED + 0.6, 2.0, 1370, 806);
fade(["s48", "s70"], T_40 + 1.0, 0.45, 1.2);
box("4TH ARTILLERY BREAKTHROUGH CORPS", 1420, 950, T_ARTY, 6.5, S4 + 3);
SFX("ref:pop", T_PACKED);
// the wide set leaves as the camera pushes in
fade(["w48", "w13", "w70", "w65", "w60", "w2ta", "g23", "g41", "g47", "g46"], T_PUSH + 0.3, 0, 0.8);
const GC = [["c23", 1505, 712, "infantry", "XXIII"], ["c41", 1410, 758, "tank", "XLI PZ"], ["c47", 1355, 756, "tank", "XLVII PZ"], ["c46", 1300, 756, "tank", "XLVI PZ"],
  ["cfd", 1442, 738, "tank", "FERDINAND"], ["cti", 1380, 728, "tank", "TIGER"]];
GC.forEach(([id, x, y, ic, lab], i) => unit(id, "rome", x, y, T_PONYRI + 1.0 + i * 0.12, { icon: ic, label: lab, fs: 4.6 }));
unit("c2ta", "carth", 1320, 945, T_PONYRI + 1.6, { icon: "tank", label: "2ND TANK ARMY", fs: 4.6 });

// ---------- close-up geography (option 2) ----------
legend("line", T_SWAP, T_OUT + 0.6);
// two-colour sector front (jul4 -> jul7), then jul7 -> jul11
const FS = K.front({ pts: KD.sector.jul4, to: KD.sector.jul7, moveT: T_BROKE, moveDur: 3.0, sideA: "carth", sideB: "rome", t: T_PUSH, dur: 1.4, width: 15, glow: 0.47, until: T_BARELY + 0.5 });
const FS2 = K.front({ pts: KD.sector.jul7, to: KD.sector.jul11, moveT: T_BARELY, moveDur: 3.0, sideA: "carth", sideB: "rome", t: T_BARELY - 0.3, dur: 0.01, width: 15, glow: 0.47, until: T_OUT + 0.4 });
// option 1 wide front of 11/12 July for the zoom-out
const FW11 = K.front({ pts: KD.wide.jul11, sideA: "carth", sideB: "rome", t: T_OUT + 0.4, dur: 1.2, width: 15 });
const CB = 6.4;  // close label size (map px)
box("PONYRI", PON[0] + 2, PON[1] + 12, T_SWAP, CB, T_OUT);
box("OLKHOVATKA", OLK[0] + 32, OLK[1] + 1, T_SWAP + 0.2, CB, T_OUT);
box("TEPLOYE", TEP[0] - 22, TEP[1] + 4, T_SWAP + 0.4, CB, T_OUT);
box("MALOARKHANGELSK", MALO[0] + 36, MALO[1] + 10, T_SWAP + 0.6, CB, T_OUT);
box("FATEZH", FAT[0], FAT[1] + 10, T_SWAP + 0.8, CB, T_OUT);
box("GLAZUNOVKA", GLAZ[0], GLAZ[1] - 10, T_SWAP + 1.0, CB, T_OUT);
[PON, OLK, TEP, MALO, FAT, GLAZ].forEach((q, i) => B.city("", ...q, { r: 2.4, t: T_SWAP + i * 0.2, until: T_OUT }));
flag(GFLAG, "GERMANY", 1240, 752, T_SWAP + 0.3, T_OUT, 30, 5.6);
flag(SFLAG, "USSR", 1530, 900, T_SWAP + 0.5, T_OUT, 30, 5.6);

// ======================= move2-4: three belts, mines, strongpoints =======================
const LL = (arr) => arr.map(([la, lo]) => G(la, lo));
const BELT1 = LL([[52.48, 36.52], [52.44, 36.47], [52.40, 36.42], [52.386, 36.38], [52.386, 36.25], [52.386, 36.10], [52.386, 35.95], [52.381, 35.80], [52.371, 35.65]]);
const BELT2 = LL([[52.36, 36.56], [52.32, 36.45], [52.30, 36.34], [52.285, 36.28], [52.258, 36.20], [52.25, 36.12], [52.245, 36.02], [52.256, 35.92], [52.29, 35.80], [52.31, 35.65]]);
const BELT3 = LL([[52.25, 36.58], [52.20, 36.45], [52.17, 36.30], [52.15, 36.15], [52.14, 36.00], [52.16, 35.85], [52.19, 35.70]]);
const belts = [BELT1, BELT2, BELT3].map((pts, i) => K.front({ pts, sideA: "carth", sideB: "carth", t: T_THREE + i * 0.7, dur: 1.6, width: 15, glow: 0.47, until: T_OUT }));
[[BELT1, "1ST BELT", 8], [BELT2, "2ND BELT", 9], [BELT3, "3RD BELT", 6]].forEach(([pts, lab, k], i) => { const q = pts[k]; box(lab, q[0] - 4, q[1] + 7, T_THREE + i * 0.7 + 0.5, 5, T_SAPPERS); SFX("ref:whoosh", T_THREE + i * 0.7); });
const mf = (n, s_, lo0, lo1) => [G(n, lo0), G(n, lo1), G(s_, lo1), G(s_, lo0)];
const MF = [mf(52.397, 52.389, 36.15, 36.36), mf(52.397, 52.389, 35.90, 36.10), mf(52.396, 52.388, 35.70, 35.86)];
MF.forEach((pg, i) => mines(pg, T_MINES + i * 0.3, T_OUT));
const MF2 = [mf(52.287, 52.278, 36.18, 36.26), mf(52.266, 52.257, 35.96, 36.09), mf(52.305, 52.296, 36.31, 36.40)];
MF2.forEach((pg, i) => mines(pg, T_MINES + 1.0 + i * 0.3, T_OUT));
SFX("ref:pop", T_MINES);
const SP = [[1320, 794], [1372, 794], [1418, 794], [1464, 784], [1340, 876], [1395, 884], [1432, 874], [1474, 852]];
SP.forEach(([x, y], i) => strong(x, y, T_STRONG + i * 0.22, i < 4 ? T_COST : T_OUT));
B.caption("THREE BELTS · MINES · ANTI-TANK STRONGPOINTS", T_THREE, S5 - 0.2, "carth");

// ======================= move2-5: night of 4/5 July, the counter-preparation =======================
const tNight = S5 - 0.6, tDawn = S6 + 0.2;
GG.night(tNight, tDawn, { dur: 2.0, outDur: 3.0 });
K.night({ lines: [FS, ...belts], tOn: tNight, tOff: tDawn });
unit("sap", "rome", 1442, 777, T_SAPPERS - 1.2, { w: 13, h: 9, icon: "infantry", label: "SAPPERS", fs: 3.6 });
K.target(1442, 777, T_SAPPERS, { r: 12, side: "carth", until: T_ZHUKOV });
SFX("static", T_SAPPERS + 0.2);
B.bubble("ATTACK AT DAWN", 1452, 790, T_DAWN_SAID, T_ZHUKOV + 0.6);
B.tl.set(B.units.sap.el.querySelector(".blk"), { backgroundColor: "#77746c" }, T_SAPPERS + 0.6);
B.hideUnits(["sap"], T_ZHUKOV + 0.4);
B.caption("ROKOSSOVSKY: OUR GUNS FIRE FIRST", T_FIRST - 0.6, T_EARLY - 0.2, "carth");
const clock = GG.card(`<div style="text-align:center"><div style="font-size:20px;letter-spacing:0.4em;color:#9fc0ea">5 JULY 1943</div><div style="font-size:96px;font-weight:700;line-height:1;letter-spacing:0.06em">02:20</div></div>`, "", 230, T_EARLY, T_HUNDREDS + 1.4);
clock.querySelector(".inner").style.borderTopColor = "#2c57b7"; SFX("hit", T_EARLY + 0.1);
// Soviet guns all along the line; shells onto the German assembly areas (every impact shakes, locked)
const GUNS = [[1305, 898], [1355, 902], [1412, 904], [1470, 884], [1384, 928], [1442, 926]];
const AA = [[1312, 752], [1378, 748], [1440, 748], [1488, 738], [1405, 728], [1350, 760], [1462, 728], [1300, 740]];
const AR_IDS = ["a4", "a1", "a2", "a3", "a5", "a6"];
for (let k = 0; k < 18; k++) {
  const gi = k % 6, t = T_HUNDREDS - 1.4 + k * 0.42, tgt = AA[(k * 3) % AA.length];
  shoot(GUNS[gi], [tgt[0] + ((k * 13) % 14) - 7, tgt[1] + ((k * 7) % 10) - 5], t, { unit: AR_IDS[gi], h: 30 + (k % 3) * 6, dur: 1.05, r: 5.5 });
}
B.caption("IT DELAYED THE ATTACK · SURPRISE WAS LOST", T_LESS, S6 - 0.3, "carth");

// ======================= move2-6: dawn 5 July, the assault =======================
GG.dawn(tDawn, S7 + 2);
// German barrage on the first belt
const GGUN = [[1350, 728], [1420, 722], [1475, 718]];
for (let k = 0; k < 6; k++) shoot(GGUN[k % 3], [1340 + ((k * 37) % 130), 795 + ((k * 11) % 14)], S6 + 0.3 + k * 0.4, { h: 26, dur: 0.9, r: 5 });
// infantry, tanks, Tigers and Ferdinands push south on a narrow front
const PUSH = [["c41", 1435, 802], ["c47", 1378, 812], ["c46", 1328, 800], ["cfd", 1458, 786], ["cti", 1405, 806], ["c23", 1488, 738]];
B.move("s13a", T_BROKE, 2.6, 1305, 846); B.move("s13b", T_BROKE, 2.6, 1398, 852); B.move("s13c", T_BROKE, 2.6, 1472, 830); B.move("s13d", T_BROKE + 0.2, 2.6, 1425, 852); B.move("s13e", T_BROKE + 0.2, 2.6, 1368, 852);
B.move("s13a", T_BARELY, 2.6, 1300, 872); B.move("s13b", T_BARELY, 2.6, 1400, 868); B.move("s13d", T_BARELY + 0.2, 2.6, 1430, 862); B.move("s13e", T_BARELY + 0.2, 2.6, 1368, 876);
PUSH.forEach(([id, x, y], i) => B.move(id, T_INTO - 0.6 + i * 0.15, 3.2, x, y));
B.arrow({ pts: [[1420, 735], [1425, 770], [1420, 812]], side: "rome", width: 4.5, t: T_INTO - 0.4, dur: 1.4, until: S7 + 1 });
B.arrow({ pts: [[1365, 735], [1370, 775], [1375, 815]], side: "rome", width: 4.5, t: T_INTO - 0.2, dur: 1.4, until: S7 + 1 });
// minefields go off under them
[[1392, 792], [1446, 796], [1338, 800], [1420, 799], [1366, 797]].forEach(([x, y], i) => K.impact(x, y, T_MINEF + i * 0.35, { r: 5, puffs: 2 }));
unit("gi1", "rome", 1405, 760, S6 + 0.4, { icon: "infantry" }); unit("gi2", "rome", 1352, 764, S6 + 0.5, { icon: "infantry" });
B.move("gi1", T_INTO - 0.4, 2.6, 1408, 798); B.move("gi2", T_INTO - 0.3, 2.6, 1352, 802);
B.grey(["gi2"], T_COST, 0.8); B.hideUnits(["gi2"], T_COST + 1.2);
B.caption("EVERY KILOMETRE COSTS MEN AND TANKS", T_COST - 0.2, S7 - 0.2, "rome");

// ======================= move2-7: Ponyri station, the fire sack =======================
K.target(PON[0], PON[1], S7 + 0.3, { r: 16, until: T_HEAVY });
B.caption("PONYRI STATION CHANGES HANDS AGAIN AND AGAIN", T_STATION - 0.6, T_LITTLE - 0.3, "");
// the station changes hands again and again: the flag on it swaps
const fl = (src) => GG.pin(`<img src="${src}" style="width:18px;display:block;border:0.6px solid #1a1712;box-shadow:0 1px 3px rgba(0,0,0,.6)">`, PON[0] - 2, PON[1] - 10, {});
const fS = fl(SFLAG), fG = fl(GFLAG);
for (let k = 0; k < 7; k++) { const t = T_STATION - 0.8 + k * 1.0, a = k % 2 ? fS : fG, b = k % 2 ? fG : fS; B.tl.to(a, { autoAlpha: 1, scale: 1, duration: 0.15 }, t); B.tl.to(b, { autoAlpha: 0, duration: 0.15 }, t); if (k % 2 === 0) K.impact(PON[0] + ((k * 7) % 12) - 6, PON[1] + ((k * 5) % 8) - 2, t - 0.15, { r: 4.5, puffs: 2 }); SFX("mg", t + 0.3); }
B.tl.to(fG, { autoAlpha: 0, duration: 0.3 }, T_STATION + 6.4); B.tl.to(fS, { autoAlpha: 1, duration: 0.3 }, T_STATION + 6.4);
B.tl.to(fS, { autoAlpha: 0, duration: 0.5 }, T_OUT);
for (let k = 0; k < 22; k++) K.smoke(PON[0] + ((k * 5) % 9) - 4, PON[1] - 2, S7 + 0.6 + k * 0.9, { n: 2, r: 4.5, rise: 16, drift: 6, alpha: 0.65 });
B.caption('"A LITTLE STALINGRAD"', T_LITTLE - 0.2, T_HEAVY - 0.2, "");
// heavy armour breaks in; the infantry behind it is cut down by the guns
B.move("cfd", T_HEAVY, 2.4, 1428, 838); B.move("c41", T_HEAVY + 0.2, 2.4, 1446, 814);
shoot([1412, 904], [1410, 806], T_CUTDOWN - 0.4, { unit: "a2", h: 14, dur: 0.6, r: 5 }); shoot([1470, 884], [1412, 798], T_CUTDOWN, { unit: "a3", h: 16, dur: 0.7, r: 5 });
B.grey(["gi1"], T_CUTDOWN + 0.6, 0.8); B.hideUnits(["gi1"], T_CUTDOWN + 1.8);
// the fire sack: guns on both flanks fire into the isolated Ferdinands
const SACK = [1428, 838];
const FL = [[1396, 852], [1462, 846]];
const FLG = FL.map(([x, y], i) => { const id = "fs" + i; unit(id, "carth", x, y, T_GREAT - 0.4, { icon: "artillery" }); return id; });
const sackRing = K.target(SACK[0], SACK[1], T_GREAT, { r: 22, side: "#ff8a3d", until: S8 + 0.5 });
for (let k = 0; k < 8; k++) { const gi = k % 2; shoot(FL[gi], [SACK[0] + ((k * 5) % 10) - 5, SACK[1] + ((k * 3) % 6) - 3], T_FLANKS - 0.6 + k * 0.45, { unit: FLG[gi], h: 8, dur: 0.45, r: 5 }); }
B.caption("FIRE SACK", T_GREAT + 0.2, S8 - 0.2, "carth");
B.tl.to(B.units.cfd.el.querySelector(".blk"), { backgroundColor: "#77746c", duration: 0.6 }, T_FLANKS + 2.2);
for (let k = 0; k < 14; k++) K.smoke(SACK[0], SACK[1] - 2, T_FLANKS + 2.0 + k * 0.7, { n: 2, r: 4, rise: 15, drift: 5, alpha: 0.7 });
unit("cfd2", "rome", 1414, 830, T_HEAVY + 0.4, { icon: "tank" }); B.tl.to(B.units.cfd2.el.querySelector(".blk"), { backgroundColor: "#77746c", duration: 0.6 }, T_CLIMB);
K.impact(1414, 830, T_CLIMB - 0.1, { r: 6, puffs: 3 });
B.hideUnits(["cfd", "cfd2", "fs0", "fs1"], S8 + 2.5, 1.0);

// ======================= move2-8: Olkhovatka heights; reserves =======================
const RIDGE = [[1325, 884], [1350, 880], [1378, 882], [1405, 878], [1428, 880]];
const rg = B.highlight(RIDGE, S8 + 0.2, S8 + 4, 16); B.tl.to(rg, { opacity: 0, duration: 0.8 }, T_WEEK2);
box("OLKHOVATKA HEIGHTS", 1378, 896, S8 + 0.4, 5.6, T_WEEK2);
unit("cres", "rome", 1340, 760, S8 - 0.2, { icon: "tank", label: "RESERVES", fs: 4.6 }); B.move("cres", T_RESERVES - 0.4, 2.2, 1350, 822);
B.move("c47", S8, 2.0, 1372, 828); B.move("c46", S8 + 0.2, 2.0, 1330, 832); B.move("cti", S8 + 0.3, 2.0, 1395, 826);
const RA = [B.arrow({ pts: [[1370, 830], [1373, 852], [1377, 870]], side: "rome", width: 5, t: T_RESERVES, dur: 1.0, until: T_RESERVES + 2.6 }),
  B.arrow({ pts: [[1332, 838], [1336, 856], [1340, 872]], side: "rome", width: 5, t: T_RESERVES + 0.5, dur: 1.0, until: T_RESERVES + 3.1 })];
K.impact(1377, 872, T_RESERVES + 1.0, { r: 6, puffs: 2 }); K.impact(1340, 874, T_RESERVES + 1.5, { r: 6, puffs: 2 }); SFX("hit", T_RESERVES + 1.1);
// Rokossovsky shifts tanks and guns from the quiet sectors
B.arrow({ pts: [[1215, 900], [1262, 892], [1318, 888]], side: "carth", width: 5, t: T_SHIFT - 0.3, dur: 1.3, until: T_BARELY + 1 });
B.arrow({ pts: [[1580, 905], [1520, 895], [1458, 880]], side: "carth", width: 5, t: T_SHIFT, dur: 1.3, until: T_BARELY + 1 });
B.move("c2ta", T_SHIFT, 2.2, 1352, 890);
unit("r2", "carth", 1225, 905, T_SHIFT - 0.4, { icon: "tank" }); B.move("r2", T_SHIFT + 0.2, 2.2, 1320, 892);
unit("r3", "carth", 1575, 912, T_SHIFT - 0.2, { icon: "artillery" }); B.move("r3", T_SHIFT + 0.4, 2.2, 1460, 890);
SFX("ref:pop", T_SHIFT);
// barely 10-15 km: bracket from the 4 July line to the furthest point
const BX = 1258, BY0 = G(52.40, 35.92)[1], BY1 = G(52.262, 36.01)[1];
GG.pin(`<svg width="14" height="${BY1 - BY0}" viewBox="0 0 14 ${BY1 - BY0}" style="display:block;overflow:visible"><path d="M12 1 L3 1 L3 ${BY1 - BY0 - 1} L12 ${BY1 - BY0 - 1}" fill="none" stroke="#1a1712" stroke-width="3"/><path d="M12 1 L3 1 L3 ${BY1 - BY0 - 1} L12 ${BY1 - BY0 - 1}" fill="none" stroke="#f7f3ea" stroke-width="1.4"/></svg>`, BX, (BY0 + BY1) / 2, { t: T_BARELY + 0.4, pop: true, until: S9 });
box("10-15 KM", BX - 26, (BY0 + BY1) / 2, T_BARELY + 0.5, 6.5, S9);
SFX("hit", T_BARELY + 0.5);
GG.stamp("STALLED", T_NOTEVEN, S9 - 0.1, { size: 56 });

// ======================= move2-9: 12 July, Operation Kutuzov (wide, option 1) =======================
fade(["c41", "c47", "c46", "cti", "c23", "cres", "s13a", "s13b", "s13c", "s13d", "s13e", "a1", "a2", "a3", "a4", "a5", "a6", "fs0", "fs1", "c2ta", "r2", "r3", "s48", "s70"], T_OUT, 0, 0.8);
box("OREL", OREL[0] + 14, OREL[1] - 32, T_OUT + 1.0, 22);
box("KURSK", KURSK[0] + 4, KURSK[1] + 34, T_OUT + 1.2, 22);
box("PONYRI", PON[0] + 60, PON[1] + 6, T_OUT + 1.4, 18);
B.city("", ...OREL, { r: 9, t: T_OUT + 1.0 }); B.city("", ...KURSK, { r: 9, t: T_OUT + 1.2 }); B.city("", ...PON, { r: 6, t: T_OUT + 1.4 });
legend("fill", T_OUT + 0.8, null);
flag(GFLAG, "GERMANY", ...G(52.6, 34.5), T_OUT + 1.0, null, 150, 30);
flag(SFLAG, "USSR", ...G(52.35, 37.55), T_OUT + 1.2, null, 150, 30);
// Kutuzov: from the north (off the top edge), toward Bolkhov, and from Novosil toward Orel
const KA = [[[G(53.80, 34.95), G(53.55, 35.25), G(53.35, 35.55)], T_ARMIES], [[G(53.72, 36.75), G(53.56, 36.35), G(53.47, 36.08)], T_ARMIES + 0.5],
  [[G(53.05, 37.25), G(52.99, 36.85), G(52.98, 36.40)], T_ARMIES + 1.0]];
KA.forEach(([pts, t]) => { B.arrow({ pts, side: "carth", width: 26, t, dur: 1.6 }); SFX("ref:whoosh", t); K.impact(pts[2][0], pts[2][1], t + 1.6, { r: 14, puffs: 3 }); });
box("OPERATION KUTUZOV", 1700, 230, T_ARMIES + 0.6, 22);
// Model pulls his divisions back north
const RET = [["k41", 1440, 800], ["k47", 1370, 820], ["k46", 1300, 820]];
RET.forEach(([id, x, y], i) => { unit(id, "rome", x, y, T_OUT + 1.0 + i * 0.15, { w: 50, h: 34, icon: "tank" }); B.move(id, T_PULL + i * 0.2, 3.0, x - 40 + i * 20, y - 210); });
B.arrow({ pts: [[1380, 760], [1370, 640], [1360, 540]], side: "rome", width: 18, t: T_PULL + 0.3, dur: 1.6, until: S10 });
GG.stamp("CITADEL FAILED", T_OVER, S10 + 1, { size: 62 }); SFX("ref:boom", T_OVER + 0.25);

// ======================= move2-10: casualties + method =======================
const pict = (k) => ({ killed: `<svg width="34" height="34" viewBox="0 0 100 100"><path d="M50 8 C24 8 12 26 12 46 C12 60 20 68 28 72 L28 88 L72 88 L72 72 C80 68 88 60 88 46 C88 26 76 8 50 8 Z" fill="#f7f3ea"/><circle cx="35" cy="46" r="10" fill="#1b1812"/><circle cx="65" cy="46" r="10" fill="#1b1812"/></svg>`,
  wounded: `<svg width="34" height="34" viewBox="0 0 100 100"><rect x="38" y="10" width="24" height="80" rx="6" fill="#f7f3ea"/><rect x="10" y="38" width="80" height="24" rx="6" fill="#f7f3ea"/><rect x="42" y="42" width="16" height="16" fill="#c4121f"/></svg>` }[k] || "");
const ccol = (src, head, c, rows) => `<div style="min-width:300px"><div style="display:flex;align-items:center;gap:12px;padding-bottom:10px;margin-bottom:10px;border-bottom:3px solid ${c}"><img src="${src}" style="height:34px;border:1px solid #f7f3ea"><div style="font-size:30px;letter-spacing:0.08em">${head}</div></div>${rows.map(([k, v, s]) => `<div style="display:flex;align-items:center;gap:14px;font-size:38px;line-height:1.45">${pict(k)}<span>${v}</span><span style="font-size:18px;letter-spacing:0.14em;color:#d8cfb8">${s}</span></div>`).join("")}</div>`;
const cas = GG.card(`<div style="display:flex;gap:60px;font-weight:700">${ccol(SFLAG, "CENTRAL FRONT", "#1f4fc4", [["killed", "15,336", "KILLED / MISSING"], ["wounded", "18,561", "WOUNDED / SICK"], ["", "33,897", "TOTAL"]])}${ccol(GFLAG, "GERMAN 9TH ARMY", "#c4121f", [["", "~20,000–23,000", ""], ["", "", "CASUALTIES, 5–12 JULY"]])}</div>`, "", 250, T_34 - 0.3, T_BEND - 0.4);
cas.querySelector(".inner").style.padding = "28px 50px 30px"; SFX("hit", T_34); SFX("hit", T_9TH);
const meth = GG.card(`<div style="font-size:26px;letter-spacing:0.4em;color:#c9b48a;text-align:center;margin-bottom:12px">ROKOSSOVSKY'S METHOD</div><div class="m1" style="font-size:60px;font-weight:700;letter-spacing:0.08em;line-height:1.35">1 · BEND, DON'T BREAK</div><div class="m2" style="font-size:60px;font-weight:700;letter-spacing:0.08em;line-height:1.35">2 · READ THE BLOW BEFORE IT LANDS</div>`, "", 300, T_BEND - 0.2, END + 1);
const m2 = meth.querySelector(".m2"); GG.hide(m2);
B.tl.fromTo(m2, { autoAlpha: 0, x: -40 }, { autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }, T_BLOW); SFX("hit", T_BEND); SFX("hit", T_BLOW);
K.raiseTerritory();
B.finish();
