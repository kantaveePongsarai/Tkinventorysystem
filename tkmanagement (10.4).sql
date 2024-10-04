-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 03, 2024 at 07:35 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tkmanagement`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `Customer_ID` int(10) NOT NULL,
  `C_name` varchar(150) NOT NULL,
  `C_surname` varchar(150) NOT NULL,
  `Identitynumber` varchar(13) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Adress` varchar(250) NOT NULL,
  `number` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`Customer_ID`, `C_name`, `C_surname`, `Identitynumber`, `Email`, `Adress`, `number`) VALUES
(1, 'สวัสดิการ', 'ขาหัก', '1231eqwe1', 'asdas23@sdq2312', '41/403 นน.ซิตี้ทาวเว่อร์คอนโดน ถ.รัตนาธิเบศ อ.เมืองนนทบุรี จ.นนทบุรี', '0971624689'),
(2, 'คนที่2', 'asdasdas', 'a213wdsa', 'asd2q2@sdasd', 'ที่อยู่ : 41/403 นน.ซิตี้ทาวเว่อร์คอนโดน ถ.รัตนาธิเบศ อ.เมืองนนทบุรี จ.นนทบุรี', '45'),
(3, 'คนที่3', 'asdasdas', '123123sadasd', 'asdasd@asdasd', 'ที่อยู่ : 41/403 นน.ซิตี้ทาวเว่อร์คอนโดน ถ.รัตนาธิเบศ อ.เมืองนนทบุรี จ.นนทบุรี', '0971624689'),
(4, 'สมหวัง', 'ฟันหลุด', '121422424', 'somwong@gmail.com', '43/100 ม.4 ต.บ้านสวน อ.เมือง จ.ชลบุรี', '0838597462'),
(5, 'สมหวังหอย', 'ฟันหลอ', '1231231231', 'iamkantavee@gmail.com', '43/100 ม.4 ต.บ้านสวน อ.เมือง จ.ชลบุรี', '0971624689'),
(6, 'asdsa', 'dasdasd', '12312312319', 'aasda@asdasd', '12/12', '0971624689'),
(7, 'asdsa', 'dasdasd', '12312312312', 'aasda@asdasd', '12/12', '0971624689'),
(8, 'กะปิเคย', 'ตรามะนาว', '1231456464', 'paratatatata@gmail.com', '4287/95 samd', '084652155'),
(9, 'สมหวัง', 'ฟันร่วงเเล้ว', '1231231231', 'iamkantavee@gmail.com', '43/100 ม.4 ต.บ้านสวน อ.เมือง จ.ชลบุรี', '0838597462');

-- --------------------------------------------------------

--
-- Table structure for table `detailseller`
--

CREATE TABLE `detailseller` (
  `Sellerdetail_ID` int(10) NOT NULL,
  `CreatedDate` date NOT NULL,
  `Pur_Orderseller_ID` int(10) NOT NULL,
  `Productstore_ID` int(10) NOT NULL,
  `quantity` float NOT NULL,
  `status` varchar(255) NOT NULL,
  `Updated` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `detailseller`
--

INSERT INTO `detailseller` (`Sellerdetail_ID`, `CreatedDate`, `Pur_Orderseller_ID`, `Productstore_ID`, `quantity`, `status`, `Updated`) VALUES
(36, '2024-06-26', 28, 1, 150, '', 1),
(37, '2024-06-26', 28, 2, 100, '', 1),
(38, '2024-06-26', 29, 1, 250, '', 1),
(39, '2024-06-26', 29, 1, 150, '', 1),
(40, '2024-07-28', 30, 2, 1, '', 1),
(41, '2024-07-28', 30, 2, 150, '', 1),
(42, '2024-07-28', 31, 3, 100, '', 1),
(43, '2024-07-28', 32, 3, 12, '', 1),
(44, '2024-07-28', 32, 2, 59, '', 1),
(45, '2024-07-28', 32, 1, 100, '', 1),
(46, '2024-07-28', 33, 3, 200, '', 1),
(47, '2024-07-28', 34, 3, 1000, '', 1),
(48, '2024-08-05', 35, 4, 2000, '', 1),
(49, '2024-08-05', 34, 5, 10, '', 1),
(50, '2024-08-12', 36, 8, 161, '', 1),
(51, '2024-09-14', 37, 1, 200, '', 1),
(52, '2024-09-14', 37, 2, 300, '', 1),
(53, '2024-09-14', 37, 4, 10, '', 1),
(54, '2024-09-14', 38, 1, 400, '', 0),
(55, '2024-09-14', 39, 2, 300, '', 0),
(56, '2024-09-15', 40, 1, 300, '', 1),
(57, '2024-09-15', 40, 2, 150, '', 1),
(58, '2024-09-20', 41, 1, 100, '', 1),
(59, '2024-09-23', 42, 1, 100, '', 0),
(60, '2024-09-26', 43, 1, 600, '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `detail_materials`
--

CREATE TABLE `detail_materials` (
  `Detail_Materials_ID` int(10) NOT NULL,
  `CreatedDate` date NOT NULL,
  `Quantity` decimal(50,2) NOT NULL,
  `Req_Materials_ID` int(10) NOT NULL,
  `Materials_ID` int(10) NOT NULL,
  `Updated` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `detail_materials`
--

INSERT INTO `detail_materials` (`Detail_Materials_ID`, `CreatedDate`, `Quantity`, `Req_Materials_ID`, `Materials_ID`, `Updated`) VALUES
(1, '2024-09-23', 1.00, 0, 1, 1),
(2, '2024-09-23', 1.00, 0, 3, 1),
(3, '2024-09-26', 1.00, 2, 9, 2),
(4, '2024-09-26', 1.00, 3, 4, 2),
(5, '2024-09-26', 5.00, 4, 1, 2),
(6, '2024-09-26', 1.00, 5, 4, 2),
(7, '2024-09-26', 1.00, 5, 3, 2),
(8, '2024-09-27', 1.00, 6, 4, 2),
(9, '2024-09-27', 1.00, 6, 3, 2),
(10, '2024-10-04', 1.00, 7, 4, 1);

-- --------------------------------------------------------

--
-- Table structure for table `materials`
--

CREATE TABLE `materials` (
  `Materials_ID` int(10) NOT NULL COMMENT 'รหัสวัสดุอุปกรณ์',
  `Materials_name` varchar(45) NOT NULL COMMENT 'ชื่อวัสดุอุปกรณ์',
  `Type` varchar(45) NOT NULL COMMENT 'ประเภทวัสดุอุปกรณ์',
  `Quantity` decimal(50,2) NOT NULL COMMENT 'จำนวน',
  `CreatedDate` date NOT NULL COMMENT 'วันที่บันทึกข้อมูล',
  `materialsimg` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `materials`
--

INSERT INTO `materials` (`Materials_ID`, `Materials_name`, `Type`, `Quantity`, `CreatedDate`, `materialsimg`) VALUES
(1, 'ตะปู', 'ก่อสร้าง', 495.00, '2024-05-24', '../static/image/P1301677.jpg'),
(2, 'ค้อนปอน', 'ค้อน', 5.00, '2024-06-25', '../static/image/36fe2025b61d002fd9ed535216191baf.jpeg'),
(3, 'ค้อน', 'ก่อสร้าง', 3.00, '2024-08-08', '../static/image/unnamed.jpg'),
(4, 'สะว่าน', 'ก่อสร้าง', 3.00, '2024-08-12', '../static/image/20160830_084732_product_2072353_big.jpg'),
(5, 'สะว่าน', 'ก่อสร้าง', 5.00, '2024-08-20', '../static/image/20160830_084732_product_2072353_big.jpg'),
(6, 'บันได', 'เส้น', 5.00, '2024-09-16', 'static/mater/51119.jpg'),
(7, 'สะว่าน', 'ก่อสร้าง', 120.00, '2024-09-16', 'static/mater/20160830_084732_product_2072353_big.jpg'),
(8, 'บันได', 'ก่อสร้าง', 100.00, '2024-09-16', 'static/mater/20160830_084732_product_2072353_big.jpg'),
(9, 'เลื่อยไฟฟ้า', 'ก่อสร้าง', 5.00, '2024-09-26', 'static/image\\36fe2025b61d002fd9ed535216191baf.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `orderdetail`
--

CREATE TABLE `orderdetail` (
  `Orderdetail_ID` int(10) NOT NULL,
  `CreatedDate` date NOT NULL,
  `Productname` varchar(255) NOT NULL,
  `UnitCost` decimal(50,2) NOT NULL,
  `Quantity` decimal(50,2) NOT NULL,
  `PurchaseOrder_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `orderdetail`
--

INSERT INTO `orderdetail` (`Orderdetail_ID`, `CreatedDate`, `Productname`, `UnitCost`, `Quantity`, `PurchaseOrder_ID`) VALUES
(1, '2024-10-04', 'เหล็กข้ออ้อย', 59.00, 100.00, 1),
(2, '2024-10-04', 'เหล็กข้ออ้อย', 100.00, 150.00, 1);

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `Payment_ID` int(10) NOT NULL,
  `Bank` varchar(45) DEFAULT NULL,
  `Payment_money` decimal(10,2) DEFAULT NULL,
  `PaymentDT` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Remark` varchar(500) DEFAULT NULL,
  `PaymentImage` text DEFAULT NULL,
  `Pur_Orderseller_ID` int(10) NOT NULL,
  `status` varchar(255) NOT NULL DEFAULT 'ยังไม่ชำระ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`Payment_ID`, `Bank`, `Payment_money`, `PaymentDT`, `Remark`, `PaymentImage`, `Pur_Orderseller_ID`, `status`) VALUES
(28, 'กสิกร', 231120.00, '2024-08-11 18:07:34', '-', 'static/bank/f02d6377-5628-4166-b9de-aaa0afeadf62.jpg', 28, 'ชำระเเล้ว'),
(29, 'กรุงไทย', 102720.00, '2024-08-11 18:08:04', '-', 'static/bank/f02d6377-5628-4166-b9de-aaa0afeadf62.jpg', 29, 'ชำระเเล้ว'),
(30, 'ไทยพาณิช', 290826.00, '2024-08-11 18:08:33', 'None', 'static/bank/f02d6377-5628-4166-b9de-aaa0afeadf62.jpg', 30, 'ชำระเเล้ว'),
(31, 'กรุงศรี', 12840.00, '2024-08-11 18:08:52', 'None', '../static/bank/faifah.jpg', 31, 'ชำระเเล้ว'),
(32, 'ออมสิน', 140854.80, '2024-08-11 18:09:13', 'None', 'static/bank/f02d6377-5628-4166-b9de-aaa0afeadf62.jpg', 32, 'ชำระเเล้ว'),
(33, 'กรุงเทพ', 25680.00, '2024-08-11 18:09:29', 'None', 'static/bank/f02d6377-5628-4166-b9de-aaa0afeadf62.jpg', 33, 'ชำระเเล้ว'),
(34, 'ทหารไทย', 129131.88, '2024-08-11 18:09:46', 'ชำระเเล้ว', 'static/bank/f02d6377-5628-4166-b9de-aaa0afeadf62.jpg', 34, 'ชำระเเล้ว'),
(35, 'ออมสิน', 513600.00, '2024-08-11 18:09:58', 'None', 'static/bank/f02d6377-5628-4166-b9de-aaa0afeadf62.jpg', 35, 'ชำระเเล้ว'),
(36, 'ออมสิน', 380000.00, '2024-08-12 02:34:19', 'ชำระผ่านธนาคารเเล้ว', 'static/bank/51119.jpg', 36, 'ชำระเเล้ว'),
(37, 'กสิกร', 51053.12, '2024-09-14 19:38:17', '-', 'static/bank/f02d6377-5628-4166-b9de-aaa0afeadf62.jpg', 37, 'ชำระเเล้ว'),
(38, NULL, NULL, '2024-09-14 22:02:43', NULL, NULL, 38, 'ยังไม่ชำระ'),
(39, NULL, NULL, '2024-09-14 23:04:36', NULL, NULL, 39, 'ยังไม่ชำระ'),
(40, 'ไทยพาณิช', 38000.00, '2024-09-15 14:27:58', '-', 'static/bank/51119.jpg', 40, 'ชำระเเล้ว'),
(41, 'กสิกร', 6088.73, '2024-09-20 11:31:27', 'ชำระเร็ว', 'static/bank/4a1578a9-1a49-4b33-83f6-db0491cd822f.jpg', 41, 'ชำระเเล้ว'),
(42, NULL, NULL, '2024-09-23 14:37:46', NULL, NULL, 42, 'ยังไม่ชำระ'),
(43, NULL, NULL, '2024-09-26 23:22:26', NULL, NULL, 43, 'ยังไม่ชำระ');

-- --------------------------------------------------------

--
-- Table structure for table `productstore`
--

CREATE TABLE `productstore` (
  `Productstore_ID` int(10) NOT NULL COMMENT 'รหัสสินค้า',
  `Pro_name` varchar(50) NOT NULL COMMENT 'ชื่อสินค้า',
  `Quantity` int(11) NOT NULL COMMENT 'จำนวนสินค้า',
  `CostAmountVat` decimal(50,2) NOT NULL COMMENT 'ราคาต้นทุนรวมภาษี',
  `AverageCost` decimal(50,2) NOT NULL COMMENT 'ราคาต้นทุนเฉลี่ยต่อชิ้น',
  `Wight` decimal(50,2) NOT NULL COMMENT 'น้ำหนัก',
  `Type_iron` text NOT NULL COMMENT 'ประเภทเหล็ก',
  `Porimage` text NOT NULL COMMENT 'รูปภาพสินค้า',
  `CreatedDate` date NOT NULL COMMENT 'วันที่บันทึกข้อมูล',
  `User_id` int(10) DEFAULT NULL,
  `Vendor_ID` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `productstore`
--

INSERT INTO `productstore` (`Productstore_ID`, `Pro_name`, `Quantity`, `CostAmountVat`, `AverageCost`, `Wight`, `Type_iron`, `Porimage`, `CreatedDate`, `User_id`, `Vendor_ID`) VALUES
(1, 'เหล็กเส้นกลม 6X10ม. SR24 พับ', 6751, 324870.00, 48.12, 2.22, 'เหล็กเส้นกลม', '../static/image/25571221_093959_product_24_800_600.jpg', '2024-05-23', 4, 2),
(2, 'เหล็กเส้นกลม 9X10ม. SR24 พับ', 8240, 815122.00, 98.92, 4.99, 'เหล็กเส้นกลม', '../static/image/25571221_093959_product_24_800_600.jpg', '2024-05-26', 1, 1),
(3, 'ข้ออ้อย 12X10ม. SD40T พับ', 1500, 238500.00, 159.00, 8.88, 'เหล็กข้ออ้อย', '../static/image/Aoy.jpg', '2024-05-23', 1, 1),
(4, 'ข้ออ้อย 12X12ม. SD40T พับ', 990, 191000.00, 192.93, 10.66, 'เหล็กข้ออ้อย', '../static/image/Aoy.jpg', '2024-06-25', 1, 1),
(5, ' ข้ออ้อย 16X10ม. SD40T พับ', 500, 139750.00, 279.50, 15.78, 'เหล็กข้ออ้อย', '../static/image/Aoy.jpg', '2024-08-04', 1, 2),
(6, ' ข้ออ้อย 16X12ม. SD40T พับ', 500, 168000.00, 336.00, 18.94, 'เหล็กข้ออ้อย', '../static/image/Aoy.jpg', '2024-08-05', 1, 1),
(7, 'ข้ออ้อย 20X10ม. SD40T พับ', 500, 218500.00, 437.00, 24.66, 'เหล็กข้ออ้อย', '../static/image/Aoy.jpg', '2024-08-05', 1, 1),
(8, 'ข้ออ้อย 20X12ม. SD40T พับ', 339, 262000.00, 772.86, 29.60, 'เหล็กข้ออ้อย', '../static/image/Aoy.jpg', '2024-08-05', 1, 1),
(9, 'ข้ออ้อย 25X10ม. SD40T พับ', 250, 172500.00, 690.00, 38.53, 'เหล็กข้ออ้อย', '../static/image/Aoy.jpg', '2024-08-05', 1, 2),
(10, 'ข้ออ้อย 25X12ม. SD40T พับ', 250, 207000.00, 828.00, 46.24, 'เหล็กข้ออ้อย', '../static/image/Aoy.jpg', '2024-08-05', 1, 1),
(11, 'เหล็กข้ออ้อย', 1212, 12312.00, 10.16, 100.00, 'เหล็กข้ออ้อย', '../static/image/ban.jpg', '2024-08-05', 1, 2),
(12, 'เหล็กเส้นเเบน', 1000, 10000.00, 10.00, 2.00, 'เหล็กเส้นเเบน', '../static/image/ban.jpg', '2024-09-12', 1, 2),
(13, 'เหล็กข้ออ้อย', 100, 45245.00, 452.45, 100.00, 'เหล็กข้ออ้อย', '../static/image/ban.jpg', '2024-09-12', 1, 1),
(14, 'เหล็กเเบน', 160, 300000.00, 1875.00, 12.20, 'เหล็กเส้นเเบน', '../static/image/ban.jpg', '2024-09-16', 1, 1),
(15, 'เหล็กข้ออ้อย', 1000, 300000.00, 300.00, 2.20, 'เหล็กเส้นกลม', '../static/image/Aoy.jpg', '2024-09-23', 1, 1),
(16, 'เหล็กข้ออ้อย', 180, 45245.00, 251.36, 2.20, 'เหล็กเส้นกลม', '../static/image/25571221_093959_product_24_800_600.jpg', '2024-09-26', 1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `purchaseorder`
--

CREATE TABLE `purchaseorder` (
  `PurchaseOrder_ID` int(10) NOT NULL,
  `CreatedDate` date NOT NULL,
  `Remark` varchar(500) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `Vendor_ID` int(11) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `purchaseorder`
--

INSERT INTO `purchaseorder` (`PurchaseOrder_ID`, `CreatedDate`, `Remark`, `total`, `User_ID`, `Vendor_ID`, `status`) VALUES
(1, '2024-10-04', '-', 22363.00, 1, 1, 'ซื้อขายสำเร็จ');

-- --------------------------------------------------------

--
-- Table structure for table `purchaseseller`
--

CREATE TABLE `purchaseseller` (
  `Pur_Orderseller_ID` int(10) NOT NULL,
  `CreatedDate` date NOT NULL,
  `DocumentDate` date NOT NULL,
  `Remark` varchar(500) NOT NULL,
  `Customer_ID` int(10) NOT NULL,
  `User_ID` int(10) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `Persenplus` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `purchaseseller`
--

INSERT INTO `purchaseseller` (`Pur_Orderseller_ID`, `CreatedDate`, `DocumentDate`, `Remark`, `Customer_ID`, `User_ID`, `total`, `Persenplus`) VALUES
(28, '2024-06-26', '2024-06-26', '-', 1, 1, 21969.24, 20),
(29, '2024-06-26', '2024-06-26', '-', 2, 2, 24302.52, 18),
(30, '2024-07-28', '2024-07-28', '-', 1, 2, 17580.75, 10),
(31, '2024-07-28', '2024-07-28', '-', 2, 2, 20415.60, 20),
(32, '2024-07-28', '2024-07-28', '-', 2, 1, 14913.09, 11),
(33, '2024-07-28', '2024-07-28', '-', 2, 1, 40831.20, 20),
(34, '2024-07-28', '2024-07-28', '-', 1, 2, 207744.78, 20),
(35, '2024-08-05', '2024-08-05', '-', 1, 1, 495444.24, 20),
(36, '2024-08-12', '2024-08-12', '-', 1, 1, 159768.71, 20),
(37, '2024-09-14', '2024-09-14', '-', 1, 3, 52938.42, 20),
(38, '2024-09-14', '2024-09-14', '-', 4, 1, 24302.52, 18),
(39, '2024-09-14', '0000-00-00', '-', 1, 1, 37468.92, 18),
(40, '2024-09-15', '0000-00-00', '-', 1, 1, 37587.82, 20),
(41, '2024-09-20', '2024-09-20', '-', 1, 1, 5663.72, 10),
(42, '2024-09-23', '2024-09-23', '-', 1, 1, 5921.17, 15),
(43, '2024-09-26', '2024-09-26', '-', 5, 2, 37071.65, 20);

-- --------------------------------------------------------

--
-- Table structure for table `requistion_materials`
--

CREATE TABLE `requistion_materials` (
  `Req_Materials_ID` int(10) NOT NULL,
  `CreatedDate` date NOT NULL,
  `Remark` varchar(500) NOT NULL,
  `status` varchar(50) NOT NULL,
  `User_ID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `requistion_materials`
--

INSERT INTO `requistion_materials` (`Req_Materials_ID`, `CreatedDate`, `Remark`, `status`, `User_ID`) VALUES
(1, '2024-09-23', 'Default Remark', 'คืนเเล้ว', 1),
(2, '2024-09-26', 'Default Remark', 'คืนเเล้ว', 3),
(3, '2024-09-26', 'Default Remark', 'คืนเเล้ว', 3),
(4, '2024-09-26', '-', 'คืนเเล้ว', 2),
(5, '2024-09-26', 'Default Remark', 'คืนเเล้ว', 3),
(6, '2024-09-27', 'Default Remark', 'คืนเเล้ว', 1),
(7, '2024-10-04', 'Default Remark', 'ยังไม่คืน', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `User_ID` int(10) NOT NULL,
  `Name` varchar(150) NOT NULL,
  `Surname` varchar(150) NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `Birthday` date NOT NULL,
  `Telenumber` varchar(20) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Position` varchar(50) NOT NULL,
  `userimage` text NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `Status_user` varchar(255) NOT NULL,
  `Remark` varchar(500) NOT NULL,
  `role` varchar(50) NOT NULL,
  `address` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`User_ID`, `Name`, `Surname`, `Gender`, `Birthday`, `Telenumber`, `Email`, `Position`, `userimage`, `username`, `password`, `Status_user`, `Remark`, `role`, `address`) VALUES
(1, 'กัณฑวีร์', 'พงษ์สาหร่าย', 'ชาย', '2000-09-18', '0971624689', 'iamkantavee@gmai.com', 'Programer', '../static/emp/IMG_20230720_233629_915.jpg', 'mon', '123', 'ยังทำงานอยู่', '-', 'admin', '484/784 kohui oko[k['),
(2, 'ฉัตรมงคล', 'เเสงสกุล', 'ชาย', '2003-05-22', '0975478456', 'asdasdwa@asdwdasd.com', 'webdeveloper', '../static/emp/1689739929263.jpg', 'jame', '123', 'ยังทำงานอยู่', '-', 'admin', 'asdsa/sadsd'),
(3, 'mamon', 'mammom', 'ชาย', '2024-05-23', '0971624689', 'kantavee@gmail.com', 'web', '../static/image/IMG_20230720_233629_915.jpg', 'mon1', '123', '', '-', 'user', '456/784 จังหวัดนนทบุรี อ.บางบัวทอง,'),
(4, 'ฉัตรมงคล', 'เเสงสกุล', 'ชาย', '2024-06-23', '0971624689', 'iamkantavee@gmail.com', 'พนักงานคลัง', '../static/emp/1689739929263.jpg', 'jame1', '123', 'ยังทำงานอยู่', '-', 'user', '58/14'),
(5, 'Kantavee', 'MaMon', 'ชาย', '2024-06-23', '0971624689', 'asda@Sdadsa', 'web', 'static/uploads/fashion_4.jpeg', '123', '123', 'ยังทำงานอยู่', '-', 'user', '256/72'),
(6, 'นายกัณฑวีร์', 'พงษ์สาหร่าย', 'ชาย', '2024-08-20', '0971624689', 'iamkantavee@gmail.com', 'พนักงานคลัง', 'static/emp/TKB2.jpg', 'mamon', '123', 'ยังทำงานอยู่', '-', 'user', '41/403 นนซิตี้ทาวเวอร์คอนโดน ชั้น7'),
(7, 'เจมส์', 'asdsad', 'ชาย', '2024-08-21', '0971624689', 'asdasA@adas', 'a1wd', '../static/emp/1689739929263.jpg', 'sa', 'ssa', 'ยังทำงานอยู่', '-', 'user', '12312/22');

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE `vendor` (
  `Vendor_ID` int(10) NOT NULL,
  `companyname` varchar(150) NOT NULL,
  `Vendorns` varchar(150) NOT NULL,
  `Identitynumber` varchar(13) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Adress` varchar(250) NOT NULL,
  `CreatedDate` date NOT NULL,
  `Remark` varchar(500) NOT NULL,
  `Telenumber` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `vendor`
--

INSERT INTO `vendor` (`Vendor_ID`, `companyname`, `Vendorns`, `Identitynumber`, `Email`, `Adress`, `CreatedDate`, `Remark`, `Telenumber`) VALUES
(1, 'จัดจำหน่ายเหล็ก', 'สุขใข เสมอหู', '123165465', 'somjit@gmail.com', '48/456  asdasd asdas asdas', '2024-06-14', '-', '0971624689'),
(2, 'สมหวังเล่น', 'หวังผล', '1200101884997', 'wdasda@asdasd.com', '43/100 ม.4 ต.บ้านสวน อ.เมือง จ.ชลบุรี', '2024-08-08', '-', '0967461234'),
(3, 'ฉัตรมงฟวย', 'มงคล', '1200101884997', 'iamkantavee@gmail.com', '43/100 ม.4 ต.บ้านสวน อ.เมือง จ.ชลบุรี', '2024-08-12', '-', '0967461234'),
(4, 'กัณฑวีร์', 'พงษ์สาหร่าย', '1200101884997', 'iamkantavee@gmail.com', '41/403 นนซิตี้', '2024-09-22', '-', '0971624689'),
(5, 'ไทวัสดุจำกัด', 'หวังผล พารวย', '1200101884223', 'asdwq@sqwd.com', '43/100 ม.4 ต.บ้านสวน อ.เมือง จ.ชลบุรี', '2024-09-26', '555', '0967461254');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`Customer_ID`);

--
-- Indexes for table `detailseller`
--
ALTER TABLE `detailseller`
  ADD PRIMARY KEY (`Sellerdetail_ID`);

--
-- Indexes for table `detail_materials`
--
ALTER TABLE `detail_materials`
  ADD PRIMARY KEY (`Detail_Materials_ID`);

--
-- Indexes for table `materials`
--
ALTER TABLE `materials`
  ADD PRIMARY KEY (`Materials_ID`);

--
-- Indexes for table `orderdetail`
--
ALTER TABLE `orderdetail`
  ADD PRIMARY KEY (`Orderdetail_ID`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`Payment_ID`);

--
-- Indexes for table `productstore`
--
ALTER TABLE `productstore`
  ADD PRIMARY KEY (`Productstore_ID`),
  ADD KEY `userpro` (`User_id`),
  ADD KEY `vendorpro` (`Vendor_ID`);

--
-- Indexes for table `purchaseorder`
--
ALTER TABLE `purchaseorder`
  ADD PRIMARY KEY (`PurchaseOrder_ID`),
  ADD KEY `userpurorder` (`User_ID`),
  ADD KEY `vendorpurorder` (`Vendor_ID`);

--
-- Indexes for table `purchaseseller`
--
ALTER TABLE `purchaseseller`
  ADD PRIMARY KEY (`Pur_Orderseller_ID`),
  ADD KEY `user` (`User_ID`),
  ADD KEY `customer` (`Customer_ID`);

--
-- Indexes for table `requistion_materials`
--
ALTER TABLE `requistion_materials`
  ADD PRIMARY KEY (`Req_Materials_ID`),
  ADD KEY `test` (`User_ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`User_ID`);

--
-- Indexes for table `vendor`
--
ALTER TABLE `vendor`
  ADD PRIMARY KEY (`Vendor_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `Customer_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `detailseller`
--
ALTER TABLE `detailseller`
  MODIFY `Sellerdetail_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `detail_materials`
--
ALTER TABLE `detail_materials`
  MODIFY `Detail_Materials_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `materials`
--
ALTER TABLE `materials`
  MODIFY `Materials_ID` int(10) NOT NULL AUTO_INCREMENT COMMENT 'รหัสวัสดุอุปกรณ์', AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `orderdetail`
--
ALTER TABLE `orderdetail`
  MODIFY `Orderdetail_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `Payment_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `productstore`
--
ALTER TABLE `productstore`
  MODIFY `Productstore_ID` int(10) NOT NULL AUTO_INCREMENT COMMENT 'รหัสสินค้า', AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `purchaseorder`
--
ALTER TABLE `purchaseorder`
  MODIFY `PurchaseOrder_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `purchaseseller`
--
ALTER TABLE `purchaseseller`
  MODIFY `Pur_Orderseller_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `requistion_materials`
--
ALTER TABLE `requistion_materials`
  MODIFY `Req_Materials_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `User_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `vendor`
--
ALTER TABLE `vendor`
  MODIFY `Vendor_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `Payment_ID` FOREIGN KEY (`Payment_ID`) REFERENCES `purchaseseller` (`Pur_Orderseller_ID`);

--
-- Constraints for table `productstore`
--
ALTER TABLE `productstore`
  ADD CONSTRAINT `userpro` FOREIGN KEY (`User_id`) REFERENCES `user` (`User_ID`),
  ADD CONSTRAINT `vendorpro` FOREIGN KEY (`Vendor_ID`) REFERENCES `vendor` (`Vendor_ID`);

--
-- Constraints for table `purchaseorder`
--
ALTER TABLE `purchaseorder`
  ADD CONSTRAINT `userpurorder` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`),
  ADD CONSTRAINT `vendorpurorder` FOREIGN KEY (`Vendor_ID`) REFERENCES `vendor` (`Vendor_ID`);

--
-- Constraints for table `purchaseseller`
--
ALTER TABLE `purchaseseller`
  ADD CONSTRAINT `customer` FOREIGN KEY (`Customer_ID`) REFERENCES `customer` (`Customer_ID`),
  ADD CONSTRAINT `user` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
