"""
India Land Rate Data Module
============================
Comprehensive land rate data for ALL 28 States + 8 Union Territories of India.
Covers 200+ cities and towns across every state/UT.
Rates are in INR per square foot.
"""

import pandas as pd
import numpy as np

INDIA_LOCATIONS = {
    # ═══ 1. ANDHRA PRADESH ═══
    "Visakhapatnam, Andhra Pradesh": (4200, 9.5, 17.6868, 83.2185, "Commercial Hub", 78),
    "Vijayawada, Andhra Pradesh": (3800, 10.2, 16.5062, 80.6480, "Emerging Market", 74),
    "Amaravati, Andhra Pradesh": (2800, 14.0, 16.5131, 80.5150, "New Capital", 65),
    "Guntur, Andhra Pradesh": (2200, 8.5, 16.3067, 80.4365, "Tier-2 City", 62),
    "Tirupati, Andhra Pradesh": (3500, 9.0, 13.6288, 79.4192, "Religious/Tourism Hub", 70),
    "Nellore, Andhra Pradesh": (1800, 7.5, 14.4426, 79.9865, "Tier-3 Town", 55),
    "Kakinada, Andhra Pradesh": (2000, 8.0, 16.9891, 82.2475, "Port City", 60),
    "Rajahmundry, Andhra Pradesh": (2400, 8.2, 17.0005, 81.8040, "Tier-2 City", 63),
    "Kurnool, Andhra Pradesh": (1500, 7.0, 15.8281, 78.0373, "Tier-3 Town", 52),
    "Anantapur, Andhra Pradesh": (1200, 6.5, 14.6819, 77.6006, "Tier-3 Town", 48),
    # ═══ 2. ARUNACHAL PRADESH ═══
    "Itanagar, Arunachal Pradesh": (1800, 7.5, 27.0844, 93.6053, "State Capital", 45),
    "Naharlagun, Arunachal Pradesh": (1400, 6.8, 27.1045, 93.6942, "Satellite Town", 40),
    "Pasighat, Arunachal Pradesh": (900, 6.0, 28.0670, 95.3269, "Tier-3 Town", 35),
    "Tawang, Arunachal Pradesh": (800, 7.0, 27.5860, 91.8597, "Tourism Hub", 32),
    # ═══ 3. ASSAM ═══
    "Guwahati, Assam": (3500, 10.0, 26.1445, 91.7362, "Commercial Hub", 72),
    "Dibrugarh, Assam": (1800, 7.5, 27.4728, 94.9120, "Tier-2 City", 55),
    "Silchar, Assam": (1500, 7.0, 24.8333, 92.7789, "Tier-2 City", 50),
    "Jorhat, Assam": (1400, 6.5, 26.7509, 94.2037, "Tier-3 Town", 48),
    "Tezpur, Assam": (1200, 6.8, 26.6338, 92.8001, "Tier-3 Town", 46),
    "Nagaon, Assam": (1000, 6.0, 26.3500, 92.6840, "Tier-3 Town", 42),
    # ═══ 4. BIHAR ═══
    "Patna, Bihar": (3800, 9.5, 25.6093, 85.1376, "State Capital", 68),
    "Gaya, Bihar": (1800, 7.5, 24.7955, 84.9994, "Religious/Tourism Hub", 52),
    "Muzaffarpur, Bihar": (1500, 7.0, 26.1197, 85.3910, "Tier-2 City", 48),
    "Bhagalpur, Bihar": (1400, 6.8, 25.2425, 86.9842, "Tier-2 City", 46),
    "Darbhanga, Bihar": (1200, 6.5, 26.1542, 85.8918, "Tier-3 Town", 44),
    "Purnia, Bihar": (1000, 7.2, 25.7771, 87.4753, "Emerging Market", 42),
    "Begusarai, Bihar": (900, 6.0, 25.4182, 86.1272, "Tier-3 Town", 40),
    "Arrah, Bihar": (1100, 6.5, 25.5541, 84.6603, "Tier-3 Town", 42),
    # ═══ 5. CHHATTISGARH ═══
    "Raipur, Chhattisgarh": (2800, 9.0, 21.2514, 81.6296, "State Capital", 68),
    "Bhilai, Chhattisgarh": (2200, 7.5, 21.2167, 81.4167, "Industrial Hub", 65),
    "Bilaspur, Chhattisgarh": (1800, 7.0, 22.0796, 82.1391, "Tier-2 City", 58),
    "Durg, Chhattisgarh": (1600, 6.8, 21.1904, 81.2849, "Tier-2 City", 56),
    "Korba, Chhattisgarh": (1200, 6.5, 22.3595, 82.7501, "Industrial Town", 50),
    "Jagdalpur, Chhattisgarh": (900, 6.0, 19.0903, 82.0208, "Tier-3 Town", 40),
    # ═══ 6. GOA ═══
    "Panaji, Goa": (8500, 8.5, 15.4909, 73.8278, "State Capital", 80),
    "Margao, Goa": (6500, 8.0, 15.2832, 73.9862, "Commercial Hub", 75),
    "Vasco da Gama, Goa": (5500, 7.5, 15.3980, 73.8113, "Port City", 72),
    "Mapusa, Goa": (5000, 7.8, 15.5935, 73.8101, "Tourism Hub", 70),
    "Calangute, Goa": (9000, 9.0, 15.5437, 73.7553, "Premium Tourism", 78),
    # ═══ 7. GUJARAT ═══
    "Ahmedabad, Gujarat": (5500, 10.5, 23.0225, 72.5714, "Metro City", 82),
    "Surat, Gujarat": (4200, 11.0, 21.1702, 72.8311, "Industrial Hub", 78),
    "Vadodara, Gujarat": (3500, 9.0, 22.3072, 73.1812, "Tier-1 City", 75),
    "Rajkot, Gujarat": (3000, 8.5, 22.3039, 70.8022, "Tier-1 City", 72),
    "Gandhinagar, Gujarat": (4800, 10.0, 23.2156, 72.6369, "State Capital", 80),
    "Bhavnagar, Gujarat": (2200, 7.0, 21.7645, 72.1519, "Tier-2 City", 60),
    "Junagadh, Gujarat": (1800, 6.5, 21.5222, 70.4579, "Tier-2 City", 55),
    "Anand, Gujarat": (2500, 8.0, 22.5645, 72.9289, "Tier-2 City", 62),
    "GIFT City, Gujarat": (7500, 14.0, 23.1547, 72.6813, "Smart City/SEZ", 90),
    "Jamnagar, Gujarat": (2000, 7.0, 22.4707, 70.0577, "Industrial Hub", 58),
    "Morbi, Gujarat": (1500, 7.5, 22.8120, 70.8370, "Industrial Town", 52),
    "Dwarka, Gujarat": (1800, 8.0, 22.2394, 68.9678, "Religious/Tourism Hub", 48),
    # ═══ 8. HARYANA ═══
    "Gurugram, Haryana": (12000, 11.0, 28.4595, 77.0266, "IT/Corporate Hub", 88),
    "Faridabad, Haryana": (5500, 8.5, 28.4089, 77.3178, "Industrial City", 75),
    "Panchkula, Haryana": (5000, 8.0, 30.6942, 76.8606, "Satellite Town", 78),
    "Ambala, Haryana": (3200, 7.5, 30.3782, 76.7767, "Tier-2 City", 65),
    "Karnal, Haryana": (2800, 8.0, 29.6857, 76.9905, "Tier-2 City", 62),
    "Panipat, Haryana": (2500, 7.5, 29.3909, 76.9635, "Industrial Town", 60),
    "Hisar, Haryana": (2200, 7.0, 29.1492, 75.7217, "Tier-2 City", 58),
    "Rohtak, Haryana": (2800, 7.5, 28.8955, 76.6066, "Tier-2 City", 60),
    "Sonipat, Haryana": (3500, 9.0, 28.9931, 77.0151, "NCR Satellite", 68),
    "Manesar, Haryana": (8000, 10.5, 28.3594, 76.9348, "Industrial/IT Hub", 82),
    # ═══ 9. HIMACHAL PRADESH ═══
    "Shimla, Himachal Pradesh": (5500, 7.5, 31.1048, 77.1734, "State Capital", 70),
    "Dharamshala, Himachal Pradesh": (4000, 8.5, 32.2190, 76.3234, "Tourism Hub", 60),
    "Manali, Himachal Pradesh": (5000, 9.0, 32.2396, 77.1887, "Premium Tourism", 58),
    "Solan, Himachal Pradesh": (3000, 7.0, 30.9045, 77.0967, "Tier-3 Town", 55),
    "Kullu, Himachal Pradesh": (3500, 7.5, 31.9579, 77.1095, "Tourism Hub", 52),
    "Mandi, Himachal Pradesh": (2200, 6.5, 31.7088, 76.9320, "Tier-3 Town", 48),
    "Kasauli, Himachal Pradesh": (4500, 8.0, 30.8984, 76.9656, "Hill Station", 55),
    # ═══ 10. JHARKHAND ═══
    "Ranchi, Jharkhand": (3200, 8.5, 23.3441, 85.3096, "State Capital", 65),
    "Jamshedpur, Jharkhand": (3500, 8.0, 22.8046, 86.2029, "Industrial Hub", 70),
    "Dhanbad, Jharkhand": (2500, 7.5, 23.7957, 86.4304, "Mining City", 58),
    "Bokaro, Jharkhand": (2000, 7.0, 23.6693, 86.1511, "Industrial Town", 60),
    "Deoghar, Jharkhand": (1500, 7.0, 24.4764, 86.6944, "Religious Town", 48),
    "Hazaribagh, Jharkhand": (1200, 6.5, 23.9966, 85.3637, "Tier-3 Town", 45),
    # ═══ 11. KARNATAKA ═══
    "Bengaluru, Karnataka": (8500, 12.0, 12.9716, 77.5946, "IT Capital", 90),
    "Mysuru, Karnataka": (3800, 9.0, 12.2958, 76.6394, "Heritage City", 75),
    "Mangaluru, Karnataka": (3500, 8.5, 12.9141, 74.8560, "Port City", 72),
    "Hubli-Dharwad, Karnataka": (2800, 8.0, 15.3647, 75.1240, "Tier-2 City", 65),
    "Belgaum (Belagavi), Karnataka": (2500, 7.5, 15.8497, 74.4977, "Tier-2 City", 62),
    "Gulbarga (Kalaburagi), Karnataka": (1800, 7.0, 17.3297, 76.8343, "Tier-2 City", 55),
    "Shimoga, Karnataka": (1500, 6.5, 13.9299, 75.5681, "Tier-3 Town", 50),
    "Tumkur, Karnataka": (2000, 7.5, 13.3392, 77.1017, "Tier-2 City", 58),
    "Whitefield, Karnataka": (9500, 12.5, 12.9698, 77.7500, "IT/Tech Hub", 88),
    "Electronic City, Karnataka": (8000, 12.0, 12.8390, 77.6770, "IT/Tech Hub", 86),
    "Udupi, Karnataka": (2200, 7.0, 13.3409, 74.7421, "Tier-3 Town", 55),
    "Davangere, Karnataka": (1600, 6.5, 14.4664, 75.9218, "Tier-3 Town", 50),
    # ═══ 12. KERALA ═══
    "Kochi, Kerala": (6500, 9.5, 9.9312, 76.2673, "Commercial Hub", 82),
    "Thiruvananthapuram, Kerala": (5000, 8.0, 8.5241, 76.9366, "State Capital", 78),
    "Kozhikode (Calicut), Kerala": (4000, 8.0, 11.2588, 75.7804, "Tier-1 City", 72),
    "Thrissur, Kerala": (3500, 7.5, 10.5276, 76.2144, "Cultural Capital", 70),
    "Kollam, Kerala": (2800, 7.0, 8.8932, 76.6141, "Tier-2 City", 65),
    "Kannur, Kerala": (3000, 7.5, 11.8745, 75.3704, "Tier-2 City", 66),
    "Alappuzha, Kerala": (3200, 7.0, 9.4981, 76.3388, "Tourism Hub", 64),
    "Palakkad, Kerala": (2500, 7.0, 10.7867, 76.6548, "Tier-2 City", 60),
    "Kottayam, Kerala": (3000, 7.0, 9.5916, 76.5222, "Tier-2 City", 65),
    "Munnar, Kerala": (4500, 8.5, 10.0889, 77.0595, "Hill Station/Tourism", 55),
    # ═══ 13. MADHYA PRADESH ═══
    "Bhopal, Madhya Pradesh": (3200, 8.5, 23.2599, 77.4126, "State Capital", 70),
    "Indore, Madhya Pradesh": (3800, 10.0, 22.7196, 75.8577, "Commercial Hub", 75),
    "Gwalior, Madhya Pradesh": (2200, 7.0, 26.2183, 78.1828, "Heritage City", 58),
    "Jabalpur, Madhya Pradesh": (2000, 7.5, 23.1815, 79.9864, "Tier-2 City", 60),
    "Ujjain, Madhya Pradesh": (1800, 7.0, 23.1765, 75.7885, "Religious City", 55),
    "Sagar, Madhya Pradesh": (1200, 6.0, 23.8388, 78.7378, "Tier-3 Town", 45),
    "Dewas, Madhya Pradesh": (1500, 6.5, 22.9623, 76.0508, "Industrial Town", 50),
    "Satna, Madhya Pradesh": (1000, 6.0, 24.5805, 80.8322, "Tier-3 Town", 42),
    "Rewa, Madhya Pradesh": (1100, 6.0, 24.5373, 81.3042, "Tier-3 Town", 44),
    # ═══ 14. MAHARASHTRA ═══
    "Mumbai, Maharashtra": (25000, 8.0, 19.0760, 72.8777, "Financial Capital", 95),
    "Pune, Maharashtra": (7500, 10.5, 18.5204, 73.8567, "IT/Education Hub", 85),
    "Navi Mumbai, Maharashtra": (8000, 11.0, 19.0330, 73.0297, "Planned City", 82),
    "Thane, Maharashtra": (7000, 9.5, 19.2183, 72.9781, "Metro Suburb", 80),
    "Nagpur, Maharashtra": (3500, 8.5, 21.1458, 79.0882, "Orange City", 72),
    "Nashik, Maharashtra": (3000, 8.0, 20.0059, 73.7798, "Tier-1 City", 68),
    "Aurangabad (Sambhajinagar), Maharashtra": (2800, 8.5, 19.8762, 75.3433, "Industrial Hub", 65),
    "Kolhapur, Maharashtra": (2500, 7.5, 16.7050, 74.2433, "Tier-2 City", 62),
    "Solapur, Maharashtra": (2000, 7.0, 17.6599, 75.9064, "Tier-2 City", 58),
    "Lonavala, Maharashtra": (6000, 9.0, 18.7546, 73.4062, "Hill Station", 65),
    "Sangli, Maharashtra": (1800, 6.5, 16.8524, 74.5815, "Tier-3 Town", 52),
    "Ratnagiri, Maharashtra": (2200, 7.0, 16.9944, 73.3000, "Coastal Town", 50),
    "Panvel, Maharashtra": (5500, 12.0, 18.9894, 73.1175, "Navi Mumbai Ext.", 75),
    "Kalyan-Dombivli, Maharashtra": (5000, 9.0, 19.2403, 73.1305, "Metro Suburb", 72),
    # ═══ 15. MANIPUR ═══
    "Imphal, Manipur": (2200, 7.5, 24.8170, 93.9368, "State Capital", 50),
    "Thoubal, Manipur": (1000, 5.5, 24.6302, 94.0162, "Tier-3 Town", 35),
    "Bishnupur, Manipur": (900, 5.0, 24.6300, 93.7700, "Heritage Town", 32),
    # ═══ 16. MEGHALAYA ═══
    "Shillong, Meghalaya": (3500, 8.0, 25.5788, 91.8933, "State Capital", 60),
    "Tura, Meghalaya": (1200, 6.0, 25.5147, 90.2097, "Tier-3 Town", 38),
    "Cherrapunji, Meghalaya": (1500, 7.5, 25.2726, 91.7323, "Tourism Spot", 35),
    # ═══ 17. MIZORAM ═══
    "Aizawl, Mizoram": (2500, 7.0, 23.7271, 92.7176, "State Capital", 48),
    "Lunglei, Mizoram": (1000, 5.5, 22.8834, 92.7312, "Tier-3 Town", 32),
    # ═══ 18. NAGALAND ═══
    "Kohima, Nagaland": (2800, 7.0, 25.6751, 94.1086, "State Capital", 48),
    "Dimapur, Nagaland": (2200, 7.5, 25.9042, 93.7266, "Commercial Center", 52),
    "Mokokchung, Nagaland": (1000, 5.5, 26.3222, 94.5203, "Tier-3 Town", 35),
    # ═══ 19. ODISHA ═══
    "Bhubaneswar, Odisha": (3800, 9.5, 20.2961, 85.8245, "State Capital", 75),
    "Cuttack, Odisha": (2800, 7.5, 20.4625, 85.8830, "Silver City", 65),
    "Puri, Odisha": (3000, 8.5, 19.7983, 85.8249, "Religious/Tourism", 62),
    "Rourkela, Odisha": (2000, 7.0, 22.2604, 84.8536, "Industrial City", 58),
    "Berhampur, Odisha": (1500, 6.5, 19.3150, 84.7941, "Tier-2 City", 52),
    "Sambalpur, Odisha": (1400, 6.5, 21.4669, 83.9756, "Tier-2 City", 50),
    # ═══ 20. PUNJAB ═══
    "Chandigarh, Punjab": (8000, 8.5, 30.7333, 76.7794, "Union Territory Capital", 85),
    "Ludhiana, Punjab": (4500, 8.0, 30.9010, 75.8573, "Industrial Hub", 72),
    "Amritsar, Punjab": (4000, 8.5, 31.6340, 74.8723, "Heritage/Tourism", 70),
    "Jalandhar, Punjab": (3200, 7.5, 31.3260, 75.5762, "Tier-1 City", 68),
    "Mohali, Punjab": (6500, 10.0, 30.7046, 76.7179, "IT City", 80),
    "Patiala, Punjab": (2800, 7.0, 30.3398, 76.3869, "Tier-2 City", 62),
    "Bathinda, Punjab": (2200, 7.0, 30.2110, 74.9455, "Tier-2 City", 55),
    "Pathankot, Punjab": (2000, 6.5, 32.2643, 75.6522, "Border Town", 50),
    "Zirakpur, Punjab": (5500, 11.0, 30.6424, 76.8173, "NCR Growth Area", 75),
    # ═══ 21. RAJASTHAN ═══
    "Jaipur, Rajasthan": (4500, 10.0, 26.9124, 75.7873, "State Capital", 78),
    "Jodhpur, Rajasthan": (2800, 8.0, 26.2389, 73.0243, "Heritage City", 65),
    "Udaipur, Rajasthan": (3500, 9.0, 24.5854, 73.7125, "Tourism Capital", 70),
    "Kota, Rajasthan": (2500, 8.5, 25.2138, 75.8648, "Education Hub", 62),
    "Ajmer, Rajasthan": (2200, 7.5, 26.4499, 74.6399, "Religious City", 58),
    "Bikaner, Rajasthan": (1800, 7.0, 28.0229, 73.3119, "Heritage Town", 52),
    "Jaisalmer, Rajasthan": (2000, 8.0, 26.9157, 70.9083, "Tourism Hub", 48),
    "Pushkar, Rajasthan": (2500, 8.5, 26.4898, 74.5511, "Tourism/Religious", 50),
    "Mount Abu, Rajasthan": (3000, 7.5, 24.5926, 72.7156, "Hill Station", 52),
    "Alwar, Rajasthan": (2000, 7.5, 27.5530, 76.6346, "NCR Influence", 55),
    "Bhilwara, Rajasthan": (1500, 6.5, 25.3407, 74.6313, "Tier-3 Town", 48),
    "Sikar, Rajasthan": (1400, 6.5, 27.6094, 75.1398, "Tier-3 Town", 45),
    # ═══ 22. SIKKIM ═══
    "Gangtok, Sikkim": (4000, 8.0, 27.3389, 88.6065, "State Capital", 58),
    "Namchi, Sikkim": (1800, 6.5, 27.1667, 88.3500, "Tourism Town", 42),
    "Pelling, Sikkim": (2200, 7.5, 27.3000, 88.2333, "Tourism Hub", 40),
    # ═══ 23. TAMIL NADU ═══
    "Chennai, Tamil Nadu": (8000, 10.0, 13.0827, 80.2707, "Metro City", 88),
    "Coimbatore, Tamil Nadu": (4500, 9.5, 11.0168, 76.9558, "Manchester of South", 78),
    "Madurai, Tamil Nadu": (3000, 8.0, 9.9252, 78.1198, "Temple City", 68),
    "Tiruchirappalli, Tamil Nadu": (2500, 7.5, 10.7905, 78.7047, "Tier-2 City", 65),
    "Salem, Tamil Nadu": (2200, 7.0, 11.6643, 78.1460, "Industrial City", 60),
    "Tirunelveli, Tamil Nadu": (1800, 6.5, 8.7139, 77.7567, "Tier-2 City", 55),
    "Vellore, Tamil Nadu": (2000, 7.0, 12.9165, 79.1325, "Education Hub", 58),
    "Erode, Tamil Nadu": (1800, 6.5, 11.3410, 77.7172, "Tier-2 City", 55),
    "Ooty (Udhagamandalam), Tamil Nadu": (5500, 8.0, 11.4102, 76.6950, "Hill Station", 55),
    "Mahabalipuram, Tamil Nadu": (3500, 9.0, 12.6269, 80.1927, "Heritage/IT Corridor", 62),
    "OMR Chennai, Tamil Nadu": (7500, 11.5, 12.9010, 80.2279, "IT Corridor", 85),
    "Hosur, Tamil Nadu": (3000, 10.0, 12.7409, 77.8253, "Industrial/IT", 68),
    "Thanjavur, Tamil Nadu": (1500, 6.0, 10.7870, 79.1378, "Heritage Town", 50),
    "Kanchipuram, Tamil Nadu": (2200, 7.5, 12.8342, 79.7036, "Temple Town", 55),
    # ═══ 24. TELANGANA ═══
    "Hyderabad, Telangana": (7500, 11.5, 17.3850, 78.4867, "IT/Corporate Hub", 88),
    "HITEC City, Telangana": (9000, 12.0, 17.4435, 78.3772, "IT Hub", 90),
    "Warangal, Telangana": (2200, 8.0, 17.9784, 79.5941, "Tier-2 City", 60),
    "Nizamabad, Telangana": (1500, 7.0, 18.6725, 78.0940, "Tier-2 City", 52),
    "Karimnagar, Telangana": (1800, 7.5, 18.4386, 79.1288, "Tier-2 City", 55),
    "Secunderabad, Telangana": (7000, 10.0, 17.4399, 78.4983, "Twin City", 85),
    "Shamshabad, Telangana": (5500, 13.0, 17.2473, 78.4269, "Airport Zone", 78),
    "Medchal, Telangana": (4000, 11.0, 17.6298, 78.4810, "Growth Corridor", 70),
    # ═══ 25. TRIPURA ═══
    "Agartala, Tripura": (2500, 7.5, 23.8315, 91.2868, "State Capital", 52),
    "Udaipur, Tripura": (1000, 5.5, 23.5339, 91.4840, "Tier-3 Town", 35),
    # ═══ 26. UTTAR PRADESH ═══
    "Noida, Uttar Pradesh": (8500, 11.0, 28.5355, 77.3910, "IT/NCR Hub", 85),
    "Greater Noida, Uttar Pradesh": (5000, 12.0, 28.4744, 77.5040, "Planned City", 78),
    "Lucknow, Uttar Pradesh": (4000, 9.5, 26.8467, 80.9462, "State Capital", 75),
    "Agra, Uttar Pradesh": (3000, 8.0, 27.1767, 78.0081, "Heritage/Tourism", 65),
    "Varanasi, Uttar Pradesh": (3500, 9.0, 25.3176, 82.9739, "Religious Capital", 68),
    "Prayagraj (Allahabad), Uttar Pradesh": (2500, 7.5, 25.4358, 81.8463, "Tier-2 City", 62),
    "Kanpur, Uttar Pradesh": (2800, 7.0, 26.4499, 80.3319, "Industrial City", 65),
    "Ghaziabad, Uttar Pradesh": (5500, 9.5, 28.6692, 77.4538, "NCR City", 78),
    "Meerut, Uttar Pradesh": (3000, 7.5, 28.9845, 77.7064, "Tier-1 City", 65),
    "Mathura, Uttar Pradesh": (2200, 8.0, 27.4924, 77.6737, "Religious Town", 55),
    "Bareilly, Uttar Pradesh": (1800, 6.5, 28.3670, 79.4304, "Tier-2 City", 52),
    "Aligarh, Uttar Pradesh": (2000, 7.0, 27.8974, 78.0880, "Education City", 55),
    "Moradabad, Uttar Pradesh": (1500, 6.5, 28.8386, 78.7733, "Brass City", 50),
    "Gorakhpur, Uttar Pradesh": (1800, 7.5, 26.7606, 83.3732, "Tier-2 City", 55),
    "Ayodhya, Uttar Pradesh": (2500, 15.0, 26.7922, 82.1998, "Religious/Emerging", 55),
    "Yamuna Expressway, Uttar Pradesh": (3500, 14.0, 28.2500, 77.5500, "Expressway Corridor", 72),
    "Jewar (Noida Airport), Uttar Pradesh": (3000, 16.0, 28.1073, 77.5552, "Airport Zone", 65),
    # ═══ 27. UTTARAKHAND ═══
    "Dehradun, Uttarakhand": (4500, 9.0, 30.3165, 78.0322, "State Capital", 72),
    "Haridwar, Uttarakhand": (3200, 8.5, 29.9457, 78.1642, "Religious City", 62),
    "Rishikesh, Uttarakhand": (3800, 9.0, 30.0869, 78.2676, "Yoga/Tourism Capital", 60),
    "Haldwani, Uttarakhand": (2500, 8.0, 29.2183, 79.5130, "Gateway City", 55),
    "Nainital, Uttarakhand": (5000, 7.5, 29.3919, 79.4542, "Hill Station", 55),
    "Mussoorie, Uttarakhand": (5500, 7.0, 30.4598, 78.0644, "Hill Station", 52),
    "Rudrapur, Uttarakhand": (2200, 8.5, 28.9737, 79.4009, "Industrial Town", 58),
    "Roorkee, Uttarakhand": (2000, 7.0, 29.8543, 77.8880, "Education Town", 55),
    # ═══ 28. WEST BENGAL ═══
    "Kolkata, West Bengal": (6500, 8.5, 22.5726, 88.3639, "Metro City", 82),
    "Salt Lake City, West Bengal": (7000, 9.5, 22.5803, 88.4120, "IT Hub", 80),
    "New Town Rajarhat, West Bengal": (5500, 11.0, 22.5958, 88.4795, "Smart City", 78),
    "Howrah, West Bengal": (4000, 7.5, 22.5958, 88.2636, "Industrial City", 72),
    "Siliguri, West Bengal": (3000, 8.5, 26.7271, 88.3953, "Gateway City", 65),
    "Durgapur, West Bengal": (2200, 7.5, 23.5204, 87.3119, "Industrial Hub", 60),
    "Asansol, West Bengal": (1800, 7.0, 23.6888, 86.9661, "Industrial City", 55),
    "Darjeeling, West Bengal": (4500, 7.0, 27.0360, 88.2627, "Hill Station", 52),
    "Kharagpur, West Bengal": (1500, 6.5, 22.3460, 87.2320, "Education Town", 50),
    "Shantiniketan, West Bengal": (2000, 7.0, 23.6814, 87.6855, "Heritage/Education", 48),
    "Digha, West Bengal": (1800, 8.0, 21.6274, 87.5451, "Beach Town", 45),
    # ═══ UNION TERRITORIES ═══
    # Delhi NCT
    "New Delhi, Delhi": (18000, 8.5, 28.6139, 77.2090, "National Capital", 95),
    "South Delhi, Delhi": (22000, 8.0, 28.5245, 77.2066, "Premium Residential", 92),
    "Dwarka, Delhi": (8500, 9.5, 28.5921, 77.0460, "Sub-City", 82),
    "Rohini, Delhi": (7000, 8.0, 28.7495, 77.0565, "Residential Hub", 78),
    "Connaught Place, Delhi": (30000, 6.5, 28.6315, 77.2167, "Premium Commercial", 98),
    "Saket, Delhi": (15000, 8.0, 28.5244, 77.2116, "Residential/Commercial", 88),
    "Lajpat Nagar, Delhi": (12000, 7.5, 28.5700, 77.2400, "Commercial Market", 82),
    # Jammu & Kashmir
    "Srinagar, Jammu & Kashmir": (4500, 8.0, 34.0837, 74.7973, "Summer Capital", 60),
    "Jammu, Jammu & Kashmir": (3800, 7.5, 32.7266, 74.8570, "Winter Capital", 62),
    "Gulmarg, Jammu & Kashmir": (5000, 9.0, 34.0484, 74.3805, "Tourism Hub", 48),
    "Pahalgam, Jammu & Kashmir": (3500, 8.0, 34.0161, 75.3150, "Tourism Hub", 42),
    # Ladakh
    "Leh, Ladakh": (3500, 9.0, 34.1526, 77.5771, "Tourism Capital", 42),
    "Kargil, Ladakh": (1500, 6.0, 34.5539, 76.1349, "Border Town", 32),
    # Puducherry
    "Puducherry (Pondicherry), Puducherry": (5500, 8.5, 11.9416, 79.8083, "UT Capital", 70),
    "Auroville, Puducherry": (4000, 7.5, 12.0058, 79.8106, "Eco Township", 60),
    # Andaman & Nicobar Islands
    "Port Blair, Andaman & Nicobar": (3500, 7.5, 11.6234, 92.7265, "UT Capital", 52),
    "Havelock Island, Andaman & Nicobar": (4000, 8.5, 12.0263, 92.9848, "Tourism Premium", 40),
    # Chandigarh
    "Chandigarh City, Chandigarh": (9000, 8.5, 30.7333, 76.7794, "Planned City", 88),
    # Dadra & Nagar Haveli and Daman & Diu
    "Silvassa, Dadra & Nagar Haveli": (2200, 8.0, 20.2766, 73.0169, "Industrial Hub", 55),
    "Daman, Daman & Diu": (2800, 7.5, 20.3974, 72.8328, "Tourism/Industrial", 52),
    "Diu, Daman & Diu": (2000, 7.0, 20.7141, 70.9876, "Tourism Town", 45),
    # Lakshadweep
    "Kavaratti, Lakshadweep": (2500, 7.0, 10.5626, 72.6369, "UT Capital", 40),
    "Agatti, Lakshadweep": (2000, 7.5, 10.8565, 72.1760, "Tourism Island", 35),
}


def get_land_rate_data():
    """Generate comprehensive land rate data for all India locations."""
    np.random.seed(42)
    years = list(range(2018, 2027))
    records = []
    for location, (base_rate, growth, lat, lon, zone, infra) in INDIA_LOCATIONS.items():
        parts = location.split(", ")
        city = parts[0]
        state = parts[1] if len(parts) > 1 else "Unknown"
        for year in years:
            years_elapsed = year - 2018
            noise = np.random.normal(0, base_rate * 0.02)
            rate = base_rate * ((1 + growth / 100) ** years_elapsed) + noise
            rate = max(rate, base_rate * 0.8)
            amenities = min(100, infra + np.random.randint(-5, 10))
            transport = min(100, infra + np.random.randint(-8, 8))
            dev_potential = max(10, 100 - infra + int(growth * 3) + np.random.randint(-5, 5))
            records.append({
                "Location": location, "City": city, "State": state,
                "Year": year, "Rate_Per_SqFt": round(rate, 2),
                "Annual_Growth_Pct": round(growth + np.random.normal(0, 0.5), 2),
                "Latitude": lat, "Longitude": lon, "Zone_Type": zone,
                "Infrastructure_Score": infra, "Amenities_Score": amenities,
                "Transport_Score": transport,
                "Development_Potential": min(100, dev_potential),
                "Population_Growth_Pct": round(np.random.uniform(0.5, 3.5), 2),
                "Employment_Index": round(np.random.uniform(60, 98), 1),
            })
    return pd.DataFrame(records)


def get_all_states():
    states = set()
    for loc in INDIA_LOCATIONS:
        parts = loc.split(", ")
        if len(parts) > 1:
            states.add(parts[1])
    return sorted(states)


def get_cities_in_state(state, df):
    return sorted(df[df["State"] == state]["City"].unique().tolist())


def get_development_factors():
    return {
        "IT Capital": {"description": "India's premier IT hub", "growth_multiplier": 1.45, "risk_level": "Medium", "key_drivers": ["IT/ITES employment", "Startup ecosystem", "Global connectivity"], "forecast": "Strong sustained growth driven by tech dominance"},
        "IT/Corporate Hub": {"description": "Major IT parks & corporate offices", "growth_multiplier": 1.40, "risk_level": "Medium", "key_drivers": ["Corporate expansion", "IT parks", "Metro connectivity"], "forecast": "Robust growth with corporate investment"},
        "IT/NCR Hub": {"description": "NCR-based IT & corporate zone", "growth_multiplier": 1.40, "risk_level": "Medium", "key_drivers": ["NCR spillover", "IT/ITES", "Expressway connectivity"], "forecast": "High growth with NCR expansion"},
        "IT Hub": {"description": "Technology park & IT zone", "growth_multiplier": 1.40, "risk_level": "Medium", "key_drivers": ["Tech parks", "IT employment", "Urban infra"], "forecast": "Strong growth with digital economy"},
        "IT/Tech Hub": {"description": "Technology & startup driven area", "growth_multiplier": 1.42, "risk_level": "Medium", "key_drivers": ["Tech companies", "Startups", "Skilled workforce"], "forecast": "Exceptional growth in tech boom"},
        "IT City": {"description": "Planned IT city with tech infra", "growth_multiplier": 1.38, "risk_level": "Medium", "key_drivers": ["IT SEZ", "Planned development", "Tech workforce"], "forecast": "Consistent tech sector growth"},
        "IT Corridor": {"description": "Extended IT corridor", "growth_multiplier": 1.38, "risk_level": "Medium", "key_drivers": ["Highway connectivity", "IT parks", "Residential demand"], "forecast": "Rapid growth as corridor matures"},
        "IT/Education Hub": {"description": "Education + IT zone", "growth_multiplier": 1.35, "risk_level": "Low-Medium", "key_drivers": ["Universities", "IT companies", "Students"], "forecast": "Steady education & tech growth"},
        "Financial Capital": {"description": "India's financial nerve center", "growth_multiplier": 1.20, "risk_level": "Low", "key_drivers": ["BFSI sector", "Corporate HQs", "Port & trade"], "forecast": "Stable premium, limited supply"},
        "National Capital": {"description": "Seat of Indian government", "growth_multiplier": 1.18, "risk_level": "Low", "key_drivers": ["Government offices", "Diplomatic enclave", "Heritage"], "forecast": "Steady appreciation"},
        "Metro City": {"description": "Major metro with diversified economy", "growth_multiplier": 1.30, "risk_level": "Low-Medium", "key_drivers": ["Diversified economy", "Metro rail", "Healthcare"], "forecast": "Balanced growth"},
        "Commercial Hub": {"description": "Major commercial center", "growth_multiplier": 1.25, "risk_level": "Low-Medium", "key_drivers": ["Trade & commerce", "Market infra", "Connectivity"], "forecast": "Consistent demand-driven growth"},
        "State Capital": {"description": "State administrative capital", "growth_multiplier": 1.25, "risk_level": "Low-Medium", "key_drivers": ["Government offices", "Admin hub", "Healthcare"], "forecast": "Steady administrative growth"},
        "New Capital": {"description": "Newly designated capital under development", "growth_multiplier": 1.55, "risk_level": "High", "key_drivers": ["Capital development", "Govt investment", "New infra"], "forecast": "Very high potential, govt dependent"},
        "Industrial Hub": {"description": "Manufacturing & production center", "growth_multiplier": 1.22, "risk_level": "Medium", "key_drivers": ["Manufacturing", "Industrial SEZ", "Employment"], "forecast": "Growth tied to Make in India"},
        "Industrial City": {"description": "City with major industrial base", "growth_multiplier": 1.20, "risk_level": "Medium", "key_drivers": ["Heavy industry", "Manufacturing", "Housing"], "forecast": "Moderate industrial growth"},
        "Industrial Town": {"description": "Town centered around industry", "growth_multiplier": 1.18, "risk_level": "Medium", "key_drivers": ["Local industry", "Employment", "Small business"], "forecast": "Growth depends on policy"},
        "Industrial/IT Hub": {"description": "Mixed industrial & IT zone", "growth_multiplier": 1.32, "risk_level": "Medium", "key_drivers": ["Industry + IT", "Mixed economy", "Connectivity"], "forecast": "Strong dual-driver growth"},
        "Industrial/IT": {"description": "Combined industrial & tech zone", "growth_multiplier": 1.30, "risk_level": "Medium", "key_drivers": ["Manufacturing", "IT parks", "Metro proximity"], "forecast": "Solid diversified growth"},
        "Planned City": {"description": "Master-planned urban development", "growth_multiplier": 1.35, "risk_level": "Low-Medium", "key_drivers": ["Urban planning", "Modern infra", "Green spaces"], "forecast": "Strong organized appreciation"},
        "Smart City/SEZ": {"description": "SEZ or Smart City mission project", "growth_multiplier": 1.50, "risk_level": "Medium", "key_drivers": ["Govt smart city funds", "SEZ incentives", "Tech infra"], "forecast": "Rapid govt-backed growth"},
        "Smart City": {"description": "Smart City mission project", "growth_multiplier": 1.38, "risk_level": "Medium", "key_drivers": ["Smart city funds", "Digital infra", "Modern planning"], "forecast": "Good govt-backed modernization"},
        "Emerging Market": {"description": "Rapidly developing area", "growth_multiplier": 1.45, "risk_level": "Medium-High", "key_drivers": ["Population influx", "New projects", "Affordable entry"], "forecast": "Highest upside with some risk"},
        "Religious/Tourism Hub": {"description": "Major religious/tourism destination", "growth_multiplier": 1.25, "risk_level": "Low-Medium", "key_drivers": ["Pilgrim traffic", "Tourism revenue", "Hotels"], "forecast": "Steady tourism growth"},
        "Religious/Tourism": {"description": "Religious pilgrimage & tourism", "growth_multiplier": 1.25, "risk_level": "Low-Medium", "key_drivers": ["Religious tourism", "Seasonal demand", "Govt investment"], "forecast": "Pilgrimage circuit growth"},
        "Religious/Emerging": {"description": "Religious town under rapid development", "growth_multiplier": 1.55, "risk_level": "Medium-High", "key_drivers": ["Temple development", "Govt projects", "Tourism growth"], "forecast": "Exceptional temple town potential"},
        "Religious Capital": {"description": "India's spiritual capital", "growth_multiplier": 1.30, "risk_level": "Low-Medium", "key_drivers": ["Religious significance", "Tourism infra", "Govt projects"], "forecast": "Strong Kashi corridor effect"},
        "Religious City": {"description": "City of religious significance", "growth_multiplier": 1.22, "risk_level": "Low-Medium", "key_drivers": ["Pilgrimage", "Temple towns", "Govt investment"], "forecast": "Moderate religious tourism growth"},
        "Religious Town": {"description": "Town centered around temples", "growth_multiplier": 1.20, "risk_level": "Low", "key_drivers": ["Pilgrimage demand", "Festivals", "Heritage"], "forecast": "Stable pilgrim footfall"},
        "Heritage City": {"description": "Rich cultural & historical heritage", "growth_multiplier": 1.22, "risk_level": "Low-Medium", "key_drivers": ["Heritage tourism", "Cultural events", "Restoration"], "forecast": "Steady heritage growth"},
        "Heritage/Tourism": {"description": "Heritage + tourism combined", "growth_multiplier": 1.24, "risk_level": "Low-Medium", "key_drivers": ["Heritage sites", "Tourism infra", "Cultural appeal"], "forecast": "Cultural tourism push"},
        "Heritage/Education": {"description": "Heritage town with universities", "growth_multiplier": 1.18, "risk_level": "Low", "key_drivers": ["University town", "Heritage value", "Culture"], "forecast": "Moderate stable growth"},
        "Heritage/IT Corridor": {"description": "Heritage area with IT development", "growth_multiplier": 1.28, "risk_level": "Medium", "key_drivers": ["Heritage tourism", "IT expansion", "Coast"], "forecast": "Tourism + tech dual drivers"},
        "Heritage Town": {"description": "Town with historical significance", "growth_multiplier": 1.15, "risk_level": "Low", "key_drivers": ["Monuments", "Tourism", "Cultural value"], "forecast": "Slow steady appreciation"},
        "Tourism Hub": {"description": "Major tourist destination", "growth_multiplier": 1.28, "risk_level": "Medium", "key_drivers": ["Tourist footfall", "Hotels", "Adventure/leisure"], "forecast": "Tourism expansion growth"},
        "Tourism Capital": {"description": "Primary tourism gateway", "growth_multiplier": 1.30, "risk_level": "Medium", "key_drivers": ["International tourism", "Adventure", "Spiritual tourism"], "forecast": "Strong global tourist growth"},
        "Tourism Spot": {"description": "Specific tourist attraction", "growth_multiplier": 1.22, "risk_level": "Medium", "key_drivers": ["Natural beauty", "Tourist infra", "Seasonal demand"], "forecast": "Moderate tourism growth"},
        "Tourism Town": {"description": "Small tourism-driven town", "growth_multiplier": 1.20, "risk_level": "Medium", "key_drivers": ["Tourist amenities", "Natural beauty", "Access"], "forecast": "Steady connectivity growth"},
        "Tourism Island": {"description": "Island tourism destination", "growth_multiplier": 1.22, "risk_level": "Medium", "key_drivers": ["Beach tourism", "Eco-tourism", "Limited supply"], "forecast": "Premium constrained growth"},
        "Tourism Premium": {"description": "Premium tourism location", "growth_multiplier": 1.28, "risk_level": "Medium", "key_drivers": ["Premium tourism", "Resorts", "Natural beauty"], "forecast": "Strong premium segment"},
        "Tourism/Industrial": {"description": "Tourism + industrial zone", "growth_multiplier": 1.22, "risk_level": "Medium", "key_drivers": ["Tourism", "Industry", "Mixed use"], "forecast": "Balanced dual growth"},
        "Tourism/Religious": {"description": "Tourism + religious destination", "growth_multiplier": 1.24, "risk_level": "Low-Medium", "key_drivers": ["Pilgrimage", "Tourism", "Heritage"], "forecast": "Cultural tourism growth"},
        "Premium Tourism": {"description": "High-end beach/resort zone", "growth_multiplier": 1.30, "risk_level": "Medium", "key_drivers": ["International tourism", "Resorts", "Beaches"], "forecast": "Premium hotspot appreciation"},
        "Premium Residential": {"description": "High-end residential area", "growth_multiplier": 1.22, "risk_level": "Low", "key_drivers": ["HNI demand", "Luxury amenities", "Location premium"], "forecast": "Steady HNI appreciation"},
        "Premium Commercial": {"description": "Premium commercial zone", "growth_multiplier": 1.15, "risk_level": "Low", "key_drivers": ["Prime location", "Corporate demand", "Limited supply"], "forecast": "Stable premium returns"},
        "Tier-1 City": {"description": "Major city with good infra", "growth_multiplier": 1.25, "risk_level": "Low-Medium", "key_drivers": ["Diversified economy", "Infrastructure", "Healthcare"], "forecast": "Consistent urban growth"},
        "Tier-2 City": {"description": "Growing city improving infra", "growth_multiplier": 1.22, "risk_level": "Medium", "key_drivers": ["Urbanization", "Govt schemes", "Affordable land"], "forecast": "Good tier-2 investment potential"},
        "Tier-3 Town": {"description": "Smaller town with basic infra", "growth_multiplier": 1.18, "risk_level": "Medium-High", "key_drivers": ["Affordable prices", "Local economy", "Connectivity"], "forecast": "Moderate project-dependent growth"},
        "Port City": {"description": "Coastal port city", "growth_multiplier": 1.22, "risk_level": "Low-Medium", "key_drivers": ["Port trade", "Logistics", "Sagarmala"], "forecast": "Maritime development growth"},
        "Satellite Town": {"description": "Town near major city", "growth_multiplier": 1.25, "risk_level": "Medium", "key_drivers": ["Metro spillover", "Affordable", "Connectivity"], "forecast": "Parent city expansion growth"},
        "NCR Satellite": {"description": "NCR satellite city", "growth_multiplier": 1.30, "risk_level": "Medium", "key_drivers": ["NCR expansion", "Expressway", "Affordable NCR"], "forecast": "Strong NCR expansion growth"},
        "NCR Growth Area": {"description": "High-growth NCR corridor", "growth_multiplier": 1.38, "risk_level": "Medium", "key_drivers": ["Expressway", "Metro expansion", "NCR demand"], "forecast": "Rapid NCR infra growth"},
        "NCR City": {"description": "Major NCR city near Delhi", "growth_multiplier": 1.28, "risk_level": "Low-Medium", "key_drivers": ["Delhi proximity", "Industrial base", "Metro"], "forecast": "Solid NCR ecosystem growth"},
        "NCR Influence": {"description": "NCR proximity benefit area", "growth_multiplier": 1.22, "risk_level": "Medium", "key_drivers": ["NCR proximity", "Highway", "Affordability"], "forecast": "Gradual NCR influence growth"},
        "Sub-City": {"description": "Planned sub-city in metro", "growth_multiplier": 1.28, "risk_level": "Low-Medium", "key_drivers": ["Metro connectivity", "Planned development", "Affordable"], "forecast": "Good metro expansion growth"},
        "Residential Hub": {"description": "Major residential area", "growth_multiplier": 1.22, "risk_level": "Low", "key_drivers": ["Housing demand", "Social infra", "Metro"], "forecast": "Steady demand-driven growth"},
        "Residential/Commercial": {"description": "Mixed residential & commercial", "growth_multiplier": 1.24, "risk_level": "Low-Medium", "key_drivers": ["Mixed use", "Commercial activity", "Residential"], "forecast": "Balanced diversified growth"},
        "Metro Suburb": {"description": "Metro city suburb", "growth_multiplier": 1.25, "risk_level": "Low-Medium", "key_drivers": ["Metro expansion", "Affordable metro", "Infra"], "forecast": "Growth with metro rail extension"},
        "Navi Mumbai Ext.": {"description": "Navi Mumbai extension near airport", "growth_multiplier": 1.40, "risk_level": "Medium", "key_drivers": ["Navi Mumbai Airport", "CIDCO", "Trans-Harbour Link"], "forecast": "Very high airport-driven growth"},
        "Commercial Market": {"description": "Traditional commercial market", "growth_multiplier": 1.18, "risk_level": "Low", "key_drivers": ["Retail trade", "Established market", "Footfall"], "forecast": "Stable limited supply"},
        "Commercial Center": {"description": "Regional commercial center", "growth_multiplier": 1.22, "risk_level": "Low-Medium", "key_drivers": ["Trade hub", "Commerce", "Business"], "forecast": "Moderate commercial growth"},
        "Mining City": {"description": "Mining & mineral extraction city", "growth_multiplier": 1.18, "risk_level": "Medium-High", "key_drivers": ["Mining", "Energy", "Industrial demand"], "forecast": "Mining sector tied growth"},
        "Education Hub": {"description": "City of educational institutions", "growth_multiplier": 1.22, "risk_level": "Low-Medium", "key_drivers": ["Students", "Coaching", "Academics"], "forecast": "Stable education growth"},
        "Education City": {"description": "Academic institutions city", "growth_multiplier": 1.20, "risk_level": "Low", "key_drivers": ["Universities", "Students", "Research"], "forecast": "Steady moderate growth"},
        "Education Town": {"description": "Town with academic campus", "growth_multiplier": 1.18, "risk_level": "Low", "key_drivers": ["Academic institution", "Student housing", "Research"], "forecast": "Moderate stable growth"},
        "Gateway City": {"description": "Gateway to larger region", "growth_multiplier": 1.25, "risk_level": "Medium", "key_drivers": ["Transit hub", "Strategic location", "Trade route"], "forecast": "Connectivity improvement growth"},
        "Silver City": {"description": "Historic silver filigree city", "growth_multiplier": 1.20, "risk_level": "Low-Medium", "key_drivers": ["Heritage", "Local industry", "Twin city"], "forecast": "Moderate twin city growth"},
        "Orange City": {"description": "Central India's major city (Nagpur)", "growth_multiplier": 1.25, "risk_level": "Low-Medium", "key_drivers": ["Central location", "MIHAN SEZ", "Expressway"], "forecast": "Strong expressway project growth"},
        "Temple City": {"description": "City famous for temples", "growth_multiplier": 1.22, "risk_level": "Low-Medium", "key_drivers": ["Temple tourism", "Heritage", "Local economy"], "forecast": "Stable cultural tourism growth"},
        "Temple Town": {"description": "Town around major temple", "growth_multiplier": 1.18, "risk_level": "Low", "key_drivers": ["Pilgrimage", "Festivals", "Heritage"], "forecast": "Steady religious tourism"},
        "Cultural Capital": {"description": "Cultural capital with arts & festivals", "growth_multiplier": 1.22, "risk_level": "Low", "key_drivers": ["Cultural events", "Pooram", "Tradition"], "forecast": "Moderate cultural growth"},
        "Manchester of South": {"description": "South India's textile & mfg hub", "growth_multiplier": 1.30, "risk_level": "Low-Medium", "key_drivers": ["Textile industry", "Manufacturing", "IT"], "forecast": "Strong industry + IT growth"},
        "Yoga/Tourism Capital": {"description": "World yoga & adventure hub", "growth_multiplier": 1.28, "risk_level": "Medium", "key_drivers": ["Yoga tourism", "Adventure sports", "International visitors"], "forecast": "Global wellness tourism growth"},
        "Summer Capital": {"description": "J&K summer capital", "growth_multiplier": 1.25, "risk_level": "Medium-High", "key_drivers": ["Tourism", "Govt activity", "Dal Lake"], "forecast": "High post-370 potential"},
        "Winter Capital": {"description": "J&K winter capital", "growth_multiplier": 1.22, "risk_level": "Medium", "key_drivers": ["Military", "Govt offices", "Transit hub"], "forecast": "Steady connectivity growth"},
        "Hill Station": {"description": "Mountain retreat & tourism", "growth_multiplier": 1.20, "risk_level": "Medium", "key_drivers": ["Tourism", "Second homes", "Climate appeal"], "forecast": "Premium limited supply growth"},
        "Hill Station/Tourism": {"description": "Hill station with tourism economy", "growth_multiplier": 1.25, "risk_level": "Medium", "key_drivers": ["Tea plantations", "Tourism", "Climate"], "forecast": "Wellness & eco-tourism growth"},
        "Beach Town": {"description": "Coastal beach tourism town", "growth_multiplier": 1.22, "risk_level": "Medium", "key_drivers": ["Beach tourism", "Weekend getaway", "Resorts"], "forecast": "Domestic tourism boom growth"},
        "Coastal Town": {"description": "Coastal fishing & tourism town", "growth_multiplier": 1.18, "risk_level": "Medium", "key_drivers": ["Coastal economy", "Tourism potential", "Fishing"], "forecast": "Moderate tourism growth"},
        "Eco Township": {"description": "Eco-friendly planned township", "growth_multiplier": 1.20, "risk_level": "Low-Medium", "key_drivers": ["Sustainable living", "International community", "Eco-tourism"], "forecast": "Niche steady appreciation"},
        "Brass City": {"description": "Brassware & handicraft city", "growth_multiplier": 1.15, "risk_level": "Medium", "key_drivers": ["Handicraft exports", "Local industry", "Trade"], "forecast": "Moderate local industry growth"},
        "Border Town": {"description": "International border town", "growth_multiplier": 1.15, "risk_level": "High", "key_drivers": ["Defense spending", "Strategic importance", "Limited growth"], "forecast": "Constrained but strategic"},
        "Airport Zone": {"description": "Area around major airport", "growth_multiplier": 1.45, "risk_level": "Medium", "key_drivers": ["Airport development", "Logistics", "Hospitality"], "forecast": "Very high airport-driven growth"},
        "Growth Corridor": {"description": "High-growth development corridor", "growth_multiplier": 1.38, "risk_level": "Medium", "key_drivers": ["Road connectivity", "New developments", "Metro"], "forecast": "Strong corridor development"},
        "Expressway Corridor": {"description": "Development along expressway", "growth_multiplier": 1.48, "risk_level": "Medium-High", "key_drivers": ["Expressway access", "Film city/Airport", "Logistics"], "forecast": "Explosive expressway growth"},
        "UT Capital": {"description": "Union Territory capital", "growth_multiplier": 1.22, "risk_level": "Low-Medium", "key_drivers": ["Admin center", "Govt investment", "Limited area"], "forecast": "Moderate central govt growth"},
        "Union Territory Capital": {"description": "UT capital serving dual states", "growth_multiplier": 1.25, "risk_level": "Low", "key_drivers": ["Planned city", "Admin center", "Quality of life"], "forecast": "Stable planned city growth"},
        "Twin City": {"description": "Twin city in metro area", "growth_multiplier": 1.30, "risk_level": "Low-Medium", "key_drivers": ["Metro connectivity", "Twin city synergy", "Commerce"], "forecast": "Strong aligned city growth"},
    }


def get_location_insights(location, df):
    loc_data = df[df["Location"] == location].sort_values("Year")
    if loc_data.empty:
        return None
    latest = loc_data.iloc[-1]
    earliest = loc_data.iloc[0]
    total_growth = ((latest["Rate_Per_SqFt"] - earliest["Rate_Per_SqFt"]) / earliest["Rate_Per_SqFt"]) * 100
    n_years = max(latest["Year"] - earliest["Year"], 1)
    return {
        "current_rate": latest["Rate_Per_SqFt"],
        "initial_rate": earliest["Rate_Per_SqFt"],
        "total_growth_pct": round(total_growth, 2),
        "avg_annual_growth": round(total_growth / n_years, 2),
        "zone_type": latest["Zone_Type"],
        "infrastructure_score": latest["Infrastructure_Score"],
        "development_potential": latest["Development_Potential"],
        "amenities_score": latest["Amenities_Score"],
        "transport_score": latest["Transport_Score"],
        "cagr": round(((latest["Rate_Per_SqFt"] / earliest["Rate_Per_SqFt"]) ** (1 / n_years) - 1) * 100, 2),
    }


# ═══════════════════════════════════════════════════════
# LEGAL RISK CHECKER MODULE
# ═══════════════════════════════════════════════════════

# State-level land law profiles
STATE_LAND_LAWS = {
    "Andhra Pradesh": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 5.0, "registration_pct": 0.5, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": True, "special_notes": "AP RERA active. Land Grabbing Prohibition Act in force."},
    "Arunachal Pradesh": {"rera_active": True, "land_ceiling_act": False, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 6.0, "registration_pct": 1.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "ILP required. Non-tribals cannot buy land. Protected under Bengal Eastern Frontier Regulation 1873."},
    "Assam": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 8.0, "registration_pct": 0.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Certain tribal belts have land transfer restrictions. NRC & land documentation issues."},
    "Bihar": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 6.0, "registration_pct": 2.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": False, "special_notes": "Poor land records. Digitization underway. Frequent title disputes."},
    "Chhattisgarh": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 5.0, "registration_pct": 4.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Scheduled Area restrictions. CNT Act applies to tribal land."},
    "Goa": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 3.5, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": True, "special_notes": "Portuguese-era land laws. Communidade (community) land issues. Strict CRZ norms."},
    "Gujarat": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Easy", "stamp_duty_pct": 4.9, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": True, "special_notes": "Online mutation. GUJRERA active. NA conversion streamlined. Tribal areas restricted."},
    "Haryana": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 7.0, "registration_pct": 0.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": False, "special_notes": "Section 118 restricts agricultural land sale. CLU (Change of Land Use) mandatory for non-agri use. HRERA very active."},
    "Himachal Pradesh": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 5.0, "registration_pct": 2.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Section 118 HP Tenancy Act – non-agriculturists CANNOT buy agri land. Tribal areas restricted. Special permission needed for outsiders."},
    "Jharkhand": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 4.0, "registration_pct": 3.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": False, "special_notes": "CNT Act & SPT Act – tribal land CANNOT be transferred to non-tribals. Strict enforcement."},
    "Karnataka": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 5.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": True, "special_notes": "Section 79A & 79B – only agriculturists can buy agri land. KRERA active. Bhoomi digital records."},
    "Kerala": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 8.0, "registration_pct": 2.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": True, "special_notes": "Strict CRZ & eco-sensitive zone. Kerala Land Reforms Act ceiling limits. Tribal land inalienable."},
    "Madhya Pradesh": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 7.5, "registration_pct": 3.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Diversion from agri land needs Collector approval. Tribal areas under PESA Act."},
    "Maharashtra": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 5.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": True, "special_notes": "MahaRERA very strict. NA conversion required. Section 36A (gairan/govt land) issues. Ready Reckoner rates apply."},
    "Manipur": {"rera_active": True, "land_ceiling_act": False, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 7.0, "registration_pct": 3.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Hill areas under customary law. Valley land under state law. Non-Manipuris restricted."},
    "Meghalaya": {"rera_active": True, "land_ceiling_act": False, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 9.9, "registration_pct": 0.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Land under Autonomous District Councils (6th Schedule). Non-tribals CANNOT buy land in most areas."},
    "Mizoram": {"rera_active": True, "land_ceiling_act": False, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 5.0, "registration_pct": 2.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "ILP required. Land under village councils/chief system. Non-Mizos cannot purchase."},
    "Nagaland": {"rera_active": True, "land_ceiling_act": False, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 8.0, "registration_pct": 2.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Article 371(A) protection. Land under tribal customary law. Non-Nagas severely restricted."},
    "Odisha": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 5.0, "registration_pct": 2.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": True, "special_notes": "OGLS Act regulates transfers. Scheduled Areas restrict tribal land sale. CRZ applies."},
    "Punjab": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 7.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": False, "special_notes": "Section 118 restrictions. Agriculturist condition for agri land. CLU required for non-agri use."},
    "Rajasthan": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 5.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Rajasthan Tenancy Act applies. Tribal sub-plan areas restricted. DLC rate governs stamp duty."},
    "Sikkim": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 6.0, "registration_pct": 1.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Revenue Order No.1 – only Sikkim Subject holders can buy land. Non-Sikkimese CANNOT purchase."},
    "Tamil Nadu": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 7.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": True, "special_notes": "TNRERA active. Hill station restrictions (Nilgiris). Patta verification essential. CRZ zones."},
    "Telangana": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Easy", "stamp_duty_pct": 5.0, "registration_pct": 0.5, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": False, "special_notes": "Dharani portal for digital land records. LRS (Layout Regularization Scheme). TSRERA active."},
    "Tripura": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 5.0, "registration_pct": 3.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": False, "special_notes": "ADC (Autonomous District Council) areas restricted. Tripura Land Revenue & Land Reforms Act applies."},
    "Uttar Pradesh": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 7.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": False, "special_notes": "UP RERA very active. Circle rate (guideline value) governs. Consolidation (chakbandi) areas frozen for transfer."},
    "Uttarakhand": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 5.0, "registration_pct": 2.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Non-domiciled CANNOT buy agri land. Hill area restrictions. Forest land issues near parks."},
    "West Bengal": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 6.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": True, "special_notes": "WBHIRA instead of RERA. Strict conversion rules. Raiyati & non-raiyati land distinction."},
    # Union Territories
    "Delhi": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 6.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": False, "special_notes": "DDA land vs Freehold. L&DO lease issues. Unauthorized colonies regularization ongoing. High litigation rate."},
    "Jammu & Kashmir": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 7.0, "registration_pct": 1.5, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Post-Article 370 abrogation – outsiders can now buy non-agri land. Agri land still restricted. Security concerns in some zones."},
    "Ladakh": {"rera_active": False, "land_ceiling_act": False, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 5.0, "registration_pct": 1.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": False, "special_notes": "UT status recent. Land laws still evolving. Tribal protections. Non-residents restricted. Strategic border area."},
    "Puducherry": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 7.0, "registration_pct": 2.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": True, "special_notes": "French-era title deeds exist. CRZ norms along coast. Guideline values updated regularly."},
    "Andaman & Nicobar": {"rera_active": False, "land_ceiling_act": True, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 5.0, "registration_pct": 1.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": True, "special_notes": "A&N Islands (Protection of Aboriginal Tribes) Regulation. Non-settlers restricted. CRZ strict. Tribal island access prohibited."},
    "Chandigarh": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 6.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": False, "special_notes": "Chandigarh Administration land. Leasehold vs freehold. Conversion charges applicable. Well-documented records."},
    "Dadra & Nagar Haveli": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 3.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": True, "coastal_zone": False, "special_notes": "Tribal population has land protection. Industrial zone land well-documented. Merged UT administration."},
    "Daman & Diu": {"rera_active": True, "land_ceiling_act": True, "agri_conversion_ease": "Moderate", "stamp_duty_pct": 3.0, "registration_pct": 1.0, "nri_allowed": True, "tribal_restriction": False, "coastal_zone": True, "special_notes": "Portuguese-era documents. CRZ norms apply. Tourism zone development rules."},
    "Lakshadweep": {"rera_active": False, "land_ceiling_act": False, "agri_conversion_ease": "Difficult", "stamp_duty_pct": 5.0, "registration_pct": 1.0, "nri_allowed": False, "tribal_restriction": True, "coastal_zone": True, "special_notes": "Lakshadweep (Protection of Scheduled Tribes) Regulation. Non-islanders CANNOT buy land. Extremely restricted."},
}

# Common legal risks applicable across India
COMMON_LEGAL_RISKS = [
    {
        "category": "Title & Ownership",
        "risks": [
            {"name": "Clear Title Verification", "description": "Ensure property has clear, undisputed title chain going back 30+ years", "severity": "Critical", "icon": "🔴"},
            {"name": "Encumbrance Certificate (EC)", "description": "Verify no mortgages, liens, pending loans, or legal charges on property", "severity": "Critical", "icon": "🔴"},
            {"name": "Succession & Inheritance Disputes", "description": "Check for pending family disputes, partition suits, or HUF property claims", "severity": "High", "icon": "🟠"},
            {"name": "Power of Attorney (PoA) Sales", "description": "GPA/SPA sales are risky – Supreme Court ruled them invalid for transfer of title", "severity": "High", "icon": "🟠"},
            {"name": "Benami Transaction", "description": "Ensure property is not held in someone else's name (Benami Transactions Act 1988)", "severity": "Critical", "icon": "🔴"},
        ],
    },
    {
        "category": "Regulatory & Compliance",
        "risks": [
            {"name": "RERA Registration", "description": "All projects >500 sqm or >8 units must be RERA registered. Check on state RERA portal", "severity": "Critical", "icon": "🔴"},
            {"name": "Building Plan Approval", "description": "Verify sanctioned plan from local body (municipal corporation/panchayat)", "severity": "High", "icon": "🟠"},
            {"name": "Occupancy Certificate (OC)", "description": "For constructed properties – OC confirms building complied with approved plans", "severity": "High", "icon": "🟠"},
            {"name": "Completion Certificate (CC)", "description": "Confirms construction is complete as per sanctioned plan", "severity": "High", "icon": "🟠"},
            {"name": "Environmental Clearance", "description": "Required for projects near forests, water bodies, eco-sensitive zones (MoEFCC)", "severity": "Medium", "icon": "🟡"},
        ],
    },
    {
        "category": "Land Classification",
        "risks": [
            {"name": "Agricultural to Non-Agricultural (NA) Conversion", "description": "Agri land MUST be converted to NA/non-agricultural before residential/commercial use", "severity": "Critical", "icon": "🔴"},
            {"name": "Government / Revenue Land", "description": "Check if land is gairan, nazar, inam, or poramboke (state-owned) – CANNOT be sold", "severity": "Critical", "icon": "🔴"},
            {"name": "Forest Land (Forest Rights Act)", "description": "Forest department land cannot be used for private purpose without central clearance", "severity": "Critical", "icon": "🔴"},
            {"name": "Ceiling Surplus Land", "description": "Land exceeding state ceiling limits may be acquired by government", "severity": "High", "icon": "🟠"},
            {"name": "Coastal Regulation Zone (CRZ)", "description": "Construction heavily restricted in CRZ-I, limited in CRZ-II & III areas", "severity": "High", "icon": "🟠"},
        ],
    },
    {
        "category": "Financial & Tax",
        "risks": [
            {"name": "Stamp Duty & Registration", "description": "Ensure correct stamp duty is paid per state rates – undervaluation attracts penalty", "severity": "High", "icon": "🟠"},
            {"name": "TDS on Property (Section 194-IA)", "description": "Buyer must deduct 1% TDS if property value exceeds ₹50 lakhs", "severity": "Medium", "icon": "🟡"},
            {"name": "Capital Gains Tax", "description": "Seller must pay LTCG (20% with indexation) or STCG on sale profits", "severity": "Medium", "icon": "🟡"},
            {"name": "Pending Property Tax", "description": "Verify no outstanding municipal property tax dues on the property", "severity": "Medium", "icon": "🟡"},
            {"name": "GST on Under-Construction", "description": "GST at 5% (non-affordable) / 1% (affordable) on under-construction property", "severity": "Medium", "icon": "🟡"},
        ],
    },
    {
        "category": "Due Diligence Checks",
        "risks": [
            {"name": "Physical Survey & Measurement", "description": "Match actual land area with documents. Engage licensed surveyor", "severity": "High", "icon": "🟠"},
            {"name": "Mutation / Khata Transfer", "description": "Revenue records must show seller as current owner (7/12 extract, Patta, Chitta)", "severity": "Critical", "icon": "🔴"},
            {"name": "Litigation Check (Lis Pendens)", "description": "Search court records for pending cases on the property", "severity": "High", "icon": "🟠"},
            {"name": "NOC from Housing Society", "description": "For resale flats – society NOC is mandatory for transfer", "severity": "Medium", "icon": "🟡"},
            {"name": "Bank Approval / Loan Eligibility", "description": "Check if major banks approve loans for the property (proxy for legitimacy)", "severity": "Medium", "icon": "🟡"},
        ],
    },
]


# City-level CRZ override: explicitly mark which cities ARE coastal (True) or NOT (False)
# Only needed for states where coastal_zone=True at state level but not all cities are coastal,
# or states where coastal_zone=False but a specific city might be coastal.
_CITY_CRZ_OVERRIDE = {
    # Karnataka: state=True, but only coastal cities actually have CRZ
    "Bengaluru, Karnataka": False,
    "Whitefield, Karnataka": False,
    "Electronic City, Karnataka": False,
    "Mysuru, Karnataka": False,
    "Hubli-Dharwad, Karnataka": False,
    "Belgaum (Belagavi), Karnataka": False,
    "Gulbarga (Kalaburagi), Karnataka": False,
    "Shimoga, Karnataka": False,
    "Tumkur, Karnataka": False,
    "Davangere, Karnataka": False,
    "Mangaluru, Karnataka": True,   # coastal
    "Udupi, Karnataka": True,       # coastal
    # Maharashtra: state=True, but only coastal/western cities
    "Pune, Maharashtra": False,
    "Nagpur, Maharashtra": False,
    "Aurangabad (Sambhajinagar), Maharashtra": False,
    "Kolhapur, Maharashtra": False,
    "Solapur, Maharashtra": False,
    "Sangli, Maharashtra": False,
    "Nashik, Maharashtra": False,
    "Lonavala, Maharashtra": False,
    "Mumbai, Maharashtra": True,
    "Navi Mumbai, Maharashtra": True,
    "Thane, Maharashtra": True,
    "Panvel, Maharashtra": True,
    "Kalyan-Dombivli, Maharashtra": False,
    "Ratnagiri, Maharashtra": True,  # coastal
    # Andhra Pradesh: state=True, only coastal cities
    "Amaravati, Andhra Pradesh": False,
    "Guntur, Andhra Pradesh": False,
    "Tirupati, Andhra Pradesh": False,
    "Kurnool, Andhra Pradesh": False,
    "Anantapur, Andhra Pradesh": False,
    "Rajahmundry, Andhra Pradesh": False,
    "Visakhapatnam, Andhra Pradesh": True,
    "Nellore, Andhra Pradesh": True,
    "Kakinada, Andhra Pradesh": True,
    "Vijayawada, Andhra Pradesh": False,
    # Tamil Nadu: state=True, only coastal cities
    "Chennai, Tamil Nadu": True,
    "OMR Chennai, Tamil Nadu": True,
    "Mahabalipuram, Tamil Nadu": True,
    "Kanchipuram, Tamil Nadu": False,
    "Coimbatore, Tamil Nadu": False,
    "Madurai, Tamil Nadu": False,
    "Tiruchirappalli, Tamil Nadu": False,
    "Salem, Tamil Nadu": False,
    "Tirunelveli, Tamil Nadu": False,
    "Vellore, Tamil Nadu": False,
    "Erode, Tamil Nadu": False,
    "Ooty (Udhagamandalam), Tamil Nadu": False,
    "Hosur, Tamil Nadu": False,
    "Thanjavur, Tamil Nadu": False,
    # Kerala: state=True, only coastal cities
    "Kochi, Kerala": True,
    "Thiruvananthapuram, Kerala": True,
    "Kozhikode (Calicut), Kerala": True,
    "Kollam, Kerala": True,
    "Kannur, Kerala": True,
    "Alappuzha, Kerala": True,
    "Thrissur, Kerala": False,
    "Palakkad, Kerala": False,
    "Kottayam, Kerala": False,
    "Munnar, Kerala": False,
    # Gujarat: state=True, only coastal
    "Ahmedabad, Gujarat": False,
    "Vadodara, Gujarat": False,
    "Gandhinagar, Gujarat": False,
    "Rajkot, Gujarat": False,
    "Anand, Gujarat": False,
    "GIFT City, Gujarat": False,
    "Morbi, Gujarat": False,
    "Surat, Gujarat": True,
    "Bhavnagar, Gujarat": True,
    "Jamnagar, Gujarat": True,
    "Junagadh, Gujarat": False,
    "Dwarka, Gujarat": True,
    # Odisha: state=True, only coastal
    "Bhubaneswar, Odisha": False,
    "Cuttack, Odisha": False,
    "Rourkela, Odisha": False,
    "Sambalpur, Odisha": False,
    "Puri, Odisha": True,
    "Berhampur, Odisha": True,
    # West Bengal: state=True, only coastal
    "Kolkata, West Bengal": False,
    "Salt Lake City, West Bengal": False,
    "New Town Rajarhat, West Bengal": False,
    "Howrah, West Bengal": False,
    "Siliguri, West Bengal": False,
    "Durgapur, West Bengal": False,
    "Asansol, West Bengal": False,
    "Darjeeling, West Bengal": False,
    "Kharagpur, West Bengal": False,
    "Shantiniketan, West Bengal": False,
    "Digha, West Bengal": True,     # beach town
    # Goa: all are near coast
    # Puducherry: coastal
    # Andaman & Nicobar: all coastal
    # Daman & Diu: coastal
    # Lakshadweep: all coastal
}

# City-level tribal restriction override: mark cities that are NOT in tribal areas
# even though state has tribal_restriction=True
_CITY_TRIBAL_OVERRIDE = {
    # Karnataka: state=False anyway, no overrides needed
    # Maharashtra: state=True, but major cities are not in tribal belts
    "Mumbai, Maharashtra": False,
    "Pune, Maharashtra": False,
    "Navi Mumbai, Maharashtra": False,
    "Thane, Maharashtra": False,
    "Nagpur, Maharashtra": False,
    "Nashik, Maharashtra": False,
    "Aurangabad (Sambhajinagar), Maharashtra": False,
    "Kolhapur, Maharashtra": False,
    "Solapur, Maharashtra": False,
    "Lonavala, Maharashtra": False,
    "Sangli, Maharashtra": False,
    "Ratnagiri, Maharashtra": False,
    "Panvel, Maharashtra": False,
    "Kalyan-Dombivli, Maharashtra": False,
    # Gujarat: state=True, only tribal belt cities
    "Ahmedabad, Gujarat": False,
    "Surat, Gujarat": False,
    "Vadodara, Gujarat": False,
    "Rajkot, Gujarat": False,
    "Gandhinagar, Gujarat": False,
    "Bhavnagar, Gujarat": False,
    "Junagadh, Gujarat": False,
    "Anand, Gujarat": False,
    "GIFT City, Gujarat": False,
    "Jamnagar, Gujarat": False,
    "Morbi, Gujarat": False,
    "Dwarka, Gujarat": False,
    # Silvassa (Dadra & Nagar Haveli) has tribal population
    # Kerala: tribal restriction mainly in Wayanad/Idukki hills
    "Kochi, Kerala": False,
    "Thiruvananthapuram, Kerala": False,
    "Kozhikode (Calicut), Kerala": False,
    "Thrissur, Kerala": False,
    "Kollam, Kerala": False,
    "Kannur, Kerala": False,
    "Alappuzha, Kerala": False,
    "Palakkad, Kerala": False,
    "Kottayam, Kerala": False,
    # Munnar is in Idukki, closer to tribal areas
    "Munnar, Kerala": True,
    # Tamil Nadu: tribal mainly in Nilgiris
    "Chennai, Tamil Nadu": False,
    "OMR Chennai, Tamil Nadu": False,
    "Coimbatore, Tamil Nadu": False,
    "Madurai, Tamil Nadu": False,
    "Tiruchirappalli, Tamil Nadu": False,
    "Salem, Tamil Nadu": False,
    "Tirunelveli, Tamil Nadu": False,
    "Vellore, Tamil Nadu": False,
    "Erode, Tamil Nadu": False,
    "Mahabalipuram, Tamil Nadu": False,
    "Hosur, Tamil Nadu": False,
    "Thanjavur, Tamil Nadu": False,
    "Kanchipuram, Tamil Nadu": False,
    "Ooty (Udhagamandalam), Tamil Nadu": True,  # Nilgiris tribal area
    # Odisha: tribal mainly in western/southern districts
    "Bhubaneswar, Odisha": False,
    "Cuttack, Odisha": False,
    "Puri, Odisha": False,
    "Berhampur, Odisha": False,
    # Rourkela/Sambalpur are near tribal areas
    # West Bengal: tribal mainly in Jangalmahal/Dooars
    "Kolkata, West Bengal": False,
    "Salt Lake City, West Bengal": False,
    "New Town Rajarhat, West Bengal": False,
    "Howrah, West Bengal": False,
    "Durgapur, West Bengal": False,
    "Asansol, West Bengal": False,
    "Darjeeling, West Bengal": False,
    "Kharagpur, West Bengal": False,
    "Shantiniketan, West Bengal": False,
    "Digha, West Bengal": False,
    "Siliguri, West Bengal": False,
    # Rajasthan: tribal mainly in southern belt (Banswara, Dungarpur, Udaipur tribal areas)
    "Jaipur, Rajasthan": False,
    "Jodhpur, Rajasthan": False,
    "Kota, Rajasthan": False,
    "Ajmer, Rajasthan": False,
    "Bikaner, Rajasthan": False,
    "Jaisalmer, Rajasthan": False,
    "Pushkar, Rajasthan": False,
    "Mount Abu, Rajasthan": True,   # tribal belt
    "Alwar, Rajasthan": False,
    "Bhilwara, Rajasthan": False,
    "Sikar, Rajasthan": False,
    "Udaipur, Rajasthan": False,    # city proper is fine; surrounding tribal
    # MP: tribal mainly in Jhabua, Mandla, Dindori etc.
    "Bhopal, Madhya Pradesh": False,
    "Indore, Madhya Pradesh": False,
    "Gwalior, Madhya Pradesh": False,
    "Jabalpur, Madhya Pradesh": False,
    "Ujjain, Madhya Pradesh": False,
    "Sagar, Madhya Pradesh": False,
    "Dewas, Madhya Pradesh": False,
    "Satna, Madhya Pradesh": False,
    "Rewa, Madhya Pradesh": False,
    # Chhattisgarh: tribal mainly in Bastar/south
    "Raipur, Chhattisgarh": False,
    "Bhilai, Chhattisgarh": False,
    "Bilaspur, Chhattisgarh": False,
    "Durg, Chhattisgarh": False,
    "Korba, Chhattisgarh": False,
    "Jagdalpur, Chhattisgarh": True,  # Bastar tribal belt
    # Jharkhand: tribal areas widespread but major cities are mixed
    "Ranchi, Jharkhand": False,
    "Jamshedpur, Jharkhand": False,
    "Dhanbad, Jharkhand": False,
    "Bokaro, Jharkhand": False,
    # Assam: tribal belts
    "Guwahati, Assam": False,
    "Dibrugarh, Assam": False,
    "Silchar, Assam": False,
    "Jorhat, Assam": False,
    "Tezpur, Assam": False,
    "Nagaon, Assam": False,
}


def get_legal_risk_profile(state, zone_type, location=None):
    """
    Generate comprehensive legal risk profile for a location based on state laws and zone type.
    Uses city-level overrides for CRZ and tribal restrictions for accuracy.
    Returns risk score, applicable risks, state-specific rules, and recommendations.
    """
    state_law = STATE_LAND_LAWS.get(state, STATE_LAND_LAWS.get("Delhi"))  # fallback

    # Create a working copy so we don't mutate the original
    state_law = dict(state_law)

    # ── Apply city-level CRZ override ──
    if location and location in _CITY_CRZ_OVERRIDE:
        state_law["coastal_zone"] = _CITY_CRZ_OVERRIDE[location]

    # ── Apply city-level tribal restriction override ──
    if location and location in _CITY_TRIBAL_OVERRIDE:
        state_law["tribal_restriction"] = _CITY_TRIBAL_OVERRIDE[location]

    # ── Calculate risk score (0–100, higher = riskier) ──
    risk_score = 30  # base

    if not state_law["rera_active"]:
        risk_score += 12
    if not state_law["nri_allowed"]:
        risk_score += 8
    if state_law["tribal_restriction"]:
        risk_score += 10
    if state_law["coastal_zone"]:
        risk_score += 5
    if state_law["agri_conversion_ease"] == "Difficult":
        risk_score += 12
    elif state_law["agri_conversion_ease"] == "Moderate":
        risk_score += 6
    if state_law["stamp_duty_pct"] >= 7:
        risk_score += 5
    if not state_law["land_ceiling_act"]:
        risk_score += 3  # less regulation = uncertain

    # Zone-type risk adjustments
    high_risk_zones = ["New Capital", "Emerging Market", "Expressway Corridor", "Airport Zone",
                       "Religious/Emerging", "Border Town", "Growth Corridor"]
    medium_risk_zones = ["Tier-3 Town", "Mining City", "Industrial Town", "Tourism Island",
                         "Beach Town", "Coastal Town", "Satellite Town"]
    low_risk_zones = ["Planned City", "Smart City/SEZ", "Financial Capital", "National Capital",
                      "IT Capital", "Premium Residential", "State Capital"]

    if zone_type in high_risk_zones:
        risk_score += 10
    elif zone_type in medium_risk_zones:
        risk_score += 5
    elif zone_type in low_risk_zones:
        risk_score -= 8

    risk_score = max(10, min(95, risk_score))

    # ── Risk Level Label ──
    if risk_score >= 70:
        risk_level = "🔴 High Risk"
        risk_color = "red"
    elif risk_score >= 50:
        risk_level = "🟠 Medium-High Risk"
        risk_color = "orange"
    elif risk_score >= 35:
        risk_level = "🟡 Moderate Risk"
        risk_color = "yellow"
    else:
        risk_level = "🟢 Low Risk"
        risk_color = "green"

    # ── State-specific warnings ──
    warnings = []
    if state_law["tribal_restriction"]:
        warnings.append("⚠️ Tribal land transfer restrictions apply in scheduled/tribal areas of this state.")
    if not state_law["nri_allowed"]:
        warnings.append("🚫 Non-residents / outsiders CANNOT purchase land in this state/UT.")
    if state_law["coastal_zone"]:
        warnings.append("🌊 CRZ (Coastal Regulation Zone) norms may restrict construction near coast.")
    if state_law["agri_conversion_ease"] == "Difficult":
        warnings.append("🌾 Agricultural land conversion is DIFFICULT – ensure NA conversion before purchase.")
    if not state_law["rera_active"]:
        warnings.append("📋 RERA may not be fully active in this UT – extra buyer caution needed.")

    # ── Recommendations ──
    recommendations = [
        "✅ Get title verified by a property lawyer (minimum 30-year chain)",
        "✅ Obtain latest Encumbrance Certificate (EC) from Sub-Registrar's office",
        f"✅ Pay correct stamp duty ({state_law['stamp_duty_pct']}%) + registration ({state_law['registration_pct']}%) charges",
        "✅ Verify mutation / khata records match seller's name",
        "✅ Check RERA registration for under-construction projects",
        "✅ Physically inspect the land and verify boundary measurements",
        "✅ Search for pending litigation on the property in local courts",
        "✅ Confirm the property is bank-loan approved (major banks)",
    ]
    if state_law["tribal_restriction"]:
        recommendations.append("✅ Verify land is NOT in a Scheduled/Tribal area before purchase")
    if state_law["coastal_zone"]:
        recommendations.append("✅ Check CRZ classification of the plot with local authority")

    # ── Required documents checklist ──
    documents = [
        "📄 Sale Deed / Title Deed",
        "📄 Encumbrance Certificate (last 30 years)",
        "📄 Property Tax Receipts (current)",
        "📄 Khata / Mutation Extract",
        "📄 Sanctioned Building Plan (if applicable)",
        "📄 Occupancy Certificate / Completion Certificate",
        "📄 RERA Registration Certificate (new projects)",
        "📄 NOC from Land Revenue / Tehsildar",
        "📄 Land Use / Zoning Certificate",
        "📄 Conversion Order (NA) – if agricultural origin",
        "📄 Survey / Measurement Map from licensed surveyor",
        "📄 Identity proof & PAN of seller",
        "📄 Society NOC (for resale flats)",
        "📄 Electricity & Water Bill (possession proof)",
    ]

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "state_law": state_law,
        "warnings": warnings,
        "recommendations": recommendations,
        "documents": documents,
        "common_risks": COMMON_LEGAL_RISKS,
        "total_duty_pct": round(state_law["stamp_duty_pct"] + state_law["registration_pct"], 2),
    }


# ═══════════════════════════════════════════════════════
# AREA RISK ALERTS MODULE
# ═══════════════════════════════════════════════════════

# Region-level environmental / area risk profiles
# Keys: state or "City, State" for city-specific overrides
# Each risk is scored 0–100 (0=no risk, 100=extreme)

_FLOOD_RISK_BY_STATE = {
    "Assam": 85, "Bihar": 80, "West Bengal": 70, "Kerala": 75, "Odisha": 72,
    "Uttar Pradesh": 55, "Uttarakhand": 60, "Andhra Pradesh": 50, "Tamil Nadu": 55,
    "Telangana": 45, "Karnataka": 40, "Maharashtra": 45, "Gujarat": 50,
    "Madhya Pradesh": 35, "Chhattisgarh": 30, "Jharkhand": 40, "Punjab": 45,
    "Haryana": 35, "Rajasthan": 20, "Himachal Pradesh": 45, "Goa": 50,
    "Tripura": 60, "Meghalaya": 65, "Manipur": 55, "Mizoram": 50,
    "Nagaland": 45, "Arunachal Pradesh": 55, "Sikkim": 50,
    "Delhi": 40, "Jammu & Kashmir": 45, "Ladakh": 25, "Puducherry": 55,
    "Andaman & Nicobar": 60, "Chandigarh": 30, "Dadra & Nagar Haveli": 35,
    "Daman & Diu": 45, "Lakshadweep": 65,
}

_WATER_SCARCITY_BY_STATE = {
    "Rajasthan": 90, "Gujarat": 60, "Maharashtra": 55, "Tamil Nadu": 65,
    "Karnataka": 60, "Telangana": 55, "Andhra Pradesh": 50, "Madhya Pradesh": 50,
    "Haryana": 55, "Punjab": 45, "Delhi": 60, "Uttar Pradesh": 45,
    "Chhattisgarh": 35, "Jharkhand": 40, "Bihar": 35, "Odisha": 30,
    "West Bengal": 25, "Kerala": 20, "Goa": 25, "Himachal Pradesh": 20,
    "Uttarakhand": 20, "Assam": 15, "Meghalaya": 15, "Tripura": 20,
    "Manipur": 20, "Mizoram": 20, "Nagaland": 25, "Arunachal Pradesh": 15,
    "Sikkim": 15, "Jammu & Kashmir": 25, "Ladakh": 70, "Puducherry": 55,
    "Andaman & Nicobar": 40, "Chandigarh": 35, "Dadra & Nagar Haveli": 35,
    "Daman & Diu": 40, "Lakshadweep": 60,
}

# City-specific flood risk overrides (higher granularity)
_FLOOD_RISK_CITY_OVERRIDE = {
    "Mumbai, Maharashtra": 82, "Chennai, Tamil Nadu": 78, "Kolkata, West Bengal": 75,
    "Patna, Bihar": 85, "Guwahati, Assam": 80, "Kochi, Kerala": 70,
    "Srinagar, Jammu & Kashmir": 72, "Hyderabad, Telangana": 60,
    "Bengaluru, Karnataka": 55, "Puri, Odisha": 78, "Alappuzha, Kerala": 82,
    "Varanasi, Uttar Pradesh": 65, "Haridwar, Uttarakhand": 68,
    "Dibrugarh, Assam": 82, "Silchar, Assam": 88,
    "Port Blair, Andaman & Nicobar": 65, "Havelock Island, Andaman & Nicobar": 60,
    "Panaji, Goa": 55, "Calangute, Goa": 52,
    "Visakhapatnam, Andhra Pradesh": 62, "Kakinada, Andhra Pradesh": 68,
    "Gorakhpur, Uttar Pradesh": 70, "Darbhanga, Bihar": 82,
    "Muzaffarpur, Bihar": 78, "Bhagalpur, Bihar": 72,
    "Agartala, Tripura": 65, "Shillong, Meghalaya": 60,
    "Imphal, Manipur": 58, "Aizawl, Mizoram": 45,
    "Digha, West Bengal": 72, "Siliguri, West Bengal": 65,
    "Nellore, Andhra Pradesh": 60, "Rajahmundry, Andhra Pradesh": 65,
}

# City-specific water scarcity overrides
_WATER_SCARCITY_CITY_OVERRIDE = {
    "Bengaluru, Karnataka": 75, "Chennai, Tamil Nadu": 80, "Hyderabad, Telangana": 62,
    "Delhi, Delhi": 70, "New Delhi, Delhi": 68, "South Delhi, Delhi": 65,
    "Jaipur, Rajasthan": 82, "Jodhpur, Rajasthan": 92, "Bikaner, Rajasthan": 95,
    "Jaisalmer, Rajasthan": 95, "Leh, Ladakh": 75, "Kargil, Ladakh": 70,
    "Coimbatore, Tamil Nadu": 60, "Madurai, Tamil Nadu": 68,
    "Nagpur, Maharashtra": 58, "Pune, Maharashtra": 48,
    "Ahmedabad, Gujarat": 65, "Rajkot, Gujarat": 70, "Bhavnagar, Gujarat": 72,
    "Indore, Madhya Pradesh": 55, "Bhopal, Madhya Pradesh": 45,
    "Gurugram, Haryana": 65, "Faridabad, Haryana": 60,
    "Noida, Uttar Pradesh": 50, "Lucknow, Uttar Pradesh": 42,
    "Anantapur, Andhra Pradesh": 78, "Kurnool, Andhra Pradesh": 72,
    "Kavaratti, Lakshadweep": 68, "Agatti, Lakshadweep": 72,
}

# Illegal layout / unauthorized colony risk data
_ILLEGAL_LAYOUT_RISK = {
    # High risk cities (known unauthorized colony / illegal layout issues)
    "Hyderabad, Telangana": {"score": 75, "details": "Thousands of LRS-pending layouts. Verify HMDA/DTCP approval.", "reported_cases": "High"},
    "Bengaluru, Karnataka": {"score": 70, "details": "BDA vs BBMP layout conflicts. Check A-khata vs B-khata status.", "reported_cases": "High"},
    "Chennai, Tamil Nadu": {"score": 60, "details": "CMDA unapproved layouts on outskirts. Check DTCP approval.", "reported_cases": "Moderate"},
    "Delhi, Delhi": {"score": 80, "details": "1,700+ unauthorized colonies. DDA regularization ongoing but many pending.", "reported_cases": "Very High"},
    "New Delhi, Delhi": {"score": 55, "details": "L&DO lease properties. Farmhouse conversion issues.", "reported_cases": "Moderate"},
    "Noida, Uttar Pradesh": {"score": 72, "details": "Builder defaults, stalled projects. Verify Noida Authority allotment.", "reported_cases": "High"},
    "Greater Noida, Uttar Pradesh": {"score": 68, "details": "Yamuna Expressway land acquisition disputes. Check authority lease.", "reported_cases": "High"},
    "Ghaziabad, Uttar Pradesh": {"score": 65, "details": "GDA layout issues. Unauthorized colonies along NH-24 & NH-58.", "reported_cases": "High"},
    "Faridabad, Haryana": {"score": 60, "details": "Aravalli zone encroachments. Check HRERA and DTCP licence.", "reported_cases": "Moderate"},
    "Gurugram, Haryana": {"score": 55, "details": "Licensed colony vs unauthorized builder issues. Verify HRERA.", "reported_cases": "Moderate"},
    "Mumbai, Maharashtra": {"score": 50, "details": "SRA slum redevelopment complications. Verify IOD/CC from BMC.", "reported_cases": "Moderate"},
    "Patna, Bihar": {"score": 70, "details": "Unauthorized colonies on agricultural land. Poor land records.", "reported_cases": "High"},
    "Lucknow, Uttar Pradesh": {"score": 58, "details": "LDA layout disputes. Gomti riverfront encroachment issues.", "reported_cases": "Moderate"},
    "Kolkata, West Bengal": {"score": 55, "details": "Panchayat area layouts often unapproved. Check KMDA approval.", "reported_cases": "Moderate"},
    "Ahmedabad, Gujarat": {"score": 45, "details": "TP scheme pending areas. Check AUDA/AMC NA status.", "reported_cases": "Low-Moderate"},
    "Pune, Maharashtra": {"score": 50, "details": "Hill slope & green zone violations. Check PMC/PCMC sanctions.", "reported_cases": "Moderate"},
    "Jaipur, Rajasthan": {"score": 55, "details": "JDA unapproved colonies. Verify JDA/Nagar Nigam layout plan.", "reported_cases": "Moderate"},
    "Amaravati, Andhra Pradesh": {"score": 65, "details": "Capital status uncertain. Land pooling scheme disputes.", "reported_cases": "High"},
    "Visakhapatnam, Andhra Pradesh": {"score": 50, "details": "VMRDA layout verification essential. Hill zone restrictions.", "reported_cases": "Moderate"},
    "Bhubaneswar, Odisha": {"score": 45, "details": "BDA approved layouts generally safe. Outskirts risky.", "reported_cases": "Low-Moderate"},
    "Ranchi, Jharkhand": {"score": 60, "details": "Tribal land sale void. Check RRDA layout approval.", "reported_cases": "Moderate"},
    "Raipur, Chhattisgarh": {"score": 48, "details": "Naya Raipur well-planned. Old Raipur layouts need RDA check.", "reported_cases": "Low-Moderate"},
    "Indore, Madhya Pradesh": {"score": 45, "details": "IDA layouts generally okay. Peripheral area risks.", "reported_cases": "Low-Moderate"},
    "Bhopal, Madhya Pradesh": {"score": 48, "details": "BDA layout verification needed. Lake area encroachments.", "reported_cases": "Low-Moderate"},
    "Ayodhya, Uttar Pradesh": {"score": 70, "details": "Rapid speculative buying. Many unauthorized plotters active.", "reported_cases": "High"},
    "Yamuna Expressway, Uttar Pradesh": {"score": 72, "details": "Unauthorized farm plots sold illegally near expressway.", "reported_cases": "High"},
    "Jewar (Noida Airport), Uttar Pradesh": {"score": 68, "details": "Speculative land grab around airport. Verify YEIDA allotment.", "reported_cases": "High"},
    "Panvel, Maharashtra": {"score": 55, "details": "CIDCO vs private layout confusion. Navi Mumbai Airport zone.", "reported_cases": "Moderate"},
    "Shamshabad, Telangana": {"score": 58, "details": "Airport zone unauthorized layouts. Verify HMDA permissions.", "reported_cases": "Moderate"},
    "Medchal, Telangana": {"score": 62, "details": "Growth corridor attracts illegal plotters. Check HMDA/DTCP.", "reported_cases": "Moderate-High"},
}

# Land dispute history profiles
_LAND_DISPUTE_HISTORY = {
    "Ayodhya, Uttar Pradesh": {"score": 80, "details": "Historic religious land disputes. New temple area land acquisition cases.", "dispute_type": "Religious/Government Acquisition"},
    "Amaravati, Andhra Pradesh": {"score": 78, "details": "Capital land pooling disputes. Farmers challenging acquisition.", "dispute_type": "Government Land Pooling"},
    "Noida, Uttar Pradesh": {"score": 75, "details": "Multiple builder insolvency (NCLT). Farmer-Authority land disputes.", "dispute_type": "Builder Default / Acquisition"},
    "Greater Noida, Uttar Pradesh": {"score": 72, "details": "Yamuna Expressway farmer protests. Builder possession delays.", "dispute_type": "Farmer / Builder Disputes"},
    "Mumbai, Maharashtra": {"score": 60, "details": "Mill land disputes. SRA/slum land litigation. Pagdi tenant issues.", "dispute_type": "Tenant / Redevelopment"},
    "Delhi, Delhi": {"score": 65, "details": "DDA acquisition disputes. Unauthorized colony regularization cases.", "dispute_type": "DDA / Unauthorized Colony"},
    "Kolkata, West Bengal": {"score": 55, "details": "Singur/Rajarhat type acquisition challenges. Vested land issues.", "dispute_type": "State Acquisition / Vested Land"},
    "Bengaluru, Karnataka": {"score": 58, "details": "Lake encroachment demolitions. BDA acquisition compensation disputes.", "dispute_type": "Encroachment / Acquisition"},
    "Hyderabad, Telangana": {"score": 55, "details": "Wakf Board land disputes. Old Nizam-era title conflicts.", "dispute_type": "Wakf / Historical Title"},
    "Chennai, Tamil Nadu": {"score": 50, "details": "Poramboke (govt) land encroachment. ECR zone disputes.", "dispute_type": "Government Land / CRZ"},
    "Goa, Goa": {"score": 52, "details": "Communidade land ownership disputes. Portuguese-era title confusion.", "dispute_type": "Community / Colonial Title"},
    "Panaji, Goa": {"score": 52, "details": "Communidade land ownership disputes. Portuguese-era title confusion.", "dispute_type": "Community / Colonial Title"},
    "Srinagar, Jammu & Kashmir": {"score": 70, "details": "Post-370 land law changes. State subject vs outsider disputes.", "dispute_type": "Constitutional / Political"},
    "Jammu, Jammu & Kashmir": {"score": 62, "details": "Roshni Act land disputes. Industrial estate issues.", "dispute_type": "Roshni Act / Industrial"},
    "Patna, Bihar": {"score": 65, "details": "Benami land holdings. Succession disputes. Poor record keeping.", "dispute_type": "Benami / Succession"},
    "Ranchi, Jharkhand": {"score": 68, "details": "CNT/SPT Act violations. Tribal vs non-tribal transfer disputes.", "dispute_type": "Tribal Land Act"},
    "Jamshedpur, Jharkhand": {"score": 55, "details": "TATA leasehold vs freehold disputes. Industrial land issues.", "dispute_type": "Leasehold / Industrial"},
    "Yamuna Expressway, Uttar Pradesh": {"score": 75, "details": "Farmer land acquisition protests. Compensation disputes.", "dispute_type": "Farmer Acquisition"},
    "Jewar (Noida Airport), Uttar Pradesh": {"score": 72, "details": "Airport area compulsory acquisition. Compensation litigation.", "dispute_type": "Airport Acquisition"},
    "Shimla, Himachal Pradesh": {"score": 50, "details": "Section 118 violations. Outsider purchase disputes.", "dispute_type": "Tenancy Act Violation"},
    "Gurugram, Haryana": {"score": 52, "details": "Licensed colony non-delivery cases. Section 118 agri-land issues.", "dispute_type": "Builder / Agri-Land"},
    "Guwahati, Assam": {"score": 58, "details": "Tribal belt land encroachment. NRC-linked land disputes.", "dispute_type": "Tribal / NRC"},
    "Imphal, Manipur": {"score": 55, "details": "Hill vs valley land law conflicts. Customary law disputes.", "dispute_type": "Customary / Constitutional"},
}

# Zone-type based proximity to development risk
_ZONE_DEV_DISTANCE = {
    "IT Capital": 0, "IT/Corporate Hub": 0, "IT Hub": 0, "IT/Tech Hub": 0,
    "Financial Capital": 0, "National Capital": 0, "Metro City": 0,
    "Commercial Hub": 5, "State Capital": 5, "IT Corridor": 5, "IT City": 5,
    "IT/NCR Hub": 5, "Planned City": 5, "Smart City/SEZ": 5,
    "Industrial Hub": 10, "Industrial City": 10, "Port City": 10,
    "NCR City": 10, "NCR Satellite": 10, "Tier-1 City": 10,
    "Twin City": 10, "Premium Residential": 5, "Premium Commercial": 0,
    "Metro Suburb": 10, "Navi Mumbai Ext.": 10, "Sub-City": 10,
    "NCR Growth Area": 15, "NCR Influence": 20, "Satellite Town": 15,
    "Emerging Market": 20, "New Capital": 20, "Growth Corridor": 15,
    "Airport Zone": 15, "Expressway Corridor": 20, "Industrial/IT Hub": 10,
    "Industrial/IT": 10, "Industrial Town": 20, "Residential Hub": 10,
    "Residential/Commercial": 10, "Commercial Center": 10, "Commercial Market": 5,
    "Tier-2 City": 20, "Education Hub": 15, "Education City": 15, "Education Town": 20,
    "Mining City": 25, "Brass City": 25, "Silver City": 15,
    "Heritage City": 15, "Heritage Town": 25, "Heritage/Tourism": 20,
    "Heritage/Education": 20, "Heritage/IT Corridor": 10, "Temple City": 20,
    "Temple Town": 25, "Cultural Capital": 15, "Orange City": 10,
    "Gateway City": 20, "Manchester of South": 10,
    "Tourism Hub": 25, "Tourism Capital": 20, "Tourism Spot": 30,
    "Tourism Town": 30, "Tourism Island": 35, "Tourism Premium": 25,
    "Tourism/Industrial": 20, "Tourism/Religious": 25, "Premium Tourism": 25,
    "Religious/Tourism Hub": 20, "Religious/Tourism": 25, "Religious/Emerging": 25,
    "Religious Capital": 15, "Religious City": 20, "Religious Town": 25,
    "Hill Station": 30, "Hill Station/Tourism": 30, "Yoga/Tourism Capital": 25,
    "Beach Town": 30, "Coastal Town": 30, "Eco Township": 25,
    "Summer Capital": 25, "Winter Capital": 20, "Border Town": 40,
    "UT Capital": 15, "Union Territory Capital": 10,
    "Tier-3 Town": 35, "Smart City": 10,
}


def get_area_risk_alerts(location, state, zone_type, infra_score, lat, lon):
    """
    Generate comprehensive area risk alerts for a given location.
    Returns risk alerts for: flood, water scarcity, illegal layouts,
    land disputes, and distance from development zones.
    """
    city_state = location  # "City, State" format
    alerts = []
    risk_scores = {}

    # ── 1. Flood Risk ──
    flood_score = _FLOOD_RISK_CITY_OVERRIDE.get(city_state, _FLOOD_RISK_BY_STATE.get(state, 30))
    # Coastal/river cities get boost
    coastal_zones = ["Port City", "Coastal Town", "Beach Town", "Tourism Island", "Premium Tourism"]
    if zone_type in coastal_zones:
        flood_score = min(100, flood_score + 12)
    risk_scores["flood"] = flood_score

    if flood_score >= 70:
        alerts.append({"type": "flood", "severity": "High", "icon": "🌊", "color": "red",
                        "title": "High Flood Risk Zone",
                        "detail": f"This area has a flood risk score of {flood_score}/100. Historical flooding reported. Verify if property is above flood line. Check NDMA flood zone maps and local drainage infrastructure.",
                        "recommendation": "Obtain flood-zone clearance certificate. Consider elevated construction. Check insurance availability."})
    elif flood_score >= 45:
        alerts.append({"type": "flood", "severity": "Moderate", "icon": "🌧️", "color": "orange",
                        "title": "Moderate Flood / Waterlogging Risk",
                        "detail": f"Flood risk score: {flood_score}/100. Seasonal waterlogging possible during monsoons. Drainage may be inadequate in some pockets.",
                        "recommendation": "Inspect drainage infrastructure. Check historical monsoon records for the specific locality."})
    else:
        alerts.append({"type": "flood", "severity": "Low", "icon": "✅", "color": "green",
                        "title": "Low Flood Risk",
                        "detail": f"Flood risk score: {flood_score}/100. Area has relatively low flood history.",
                        "recommendation": "Standard precautions sufficient. Verify local nala/drain proximity."})

    # ── 2. Water Scarcity ──
    water_score = _WATER_SCARCITY_CITY_OVERRIDE.get(city_state, _WATER_SCARCITY_BY_STATE.get(state, 40))
    # Arid zones
    if zone_type in ["Border Town"] or state in ["Rajasthan", "Ladakh"]:
        water_score = min(100, water_score + 8)
    risk_scores["water_scarcity"] = water_score

    if water_score >= 70:
        alerts.append({"type": "water_scarcity", "severity": "High", "icon": "🏜️", "color": "red",
                        "title": "Severe Water Scarcity Zone",
                        "detail": f"Water scarcity score: {water_score}/100. Groundwater depletion & irregular municipal supply reported. May need tanker water or borewell.",
                        "recommendation": "Check CGWB groundwater level data. Verify municipal water connection. Budget for water storage & RO system."})
    elif water_score >= 45:
        alerts.append({"type": "water_scarcity", "severity": "Moderate", "icon": "💧", "color": "orange",
                        "title": "Moderate Water Stress",
                        "detail": f"Water scarcity score: {water_score}/100. Seasonal water shortages possible, especially summer. Groundwater levels declining.",
                        "recommendation": "Verify water supply hours. Check borewell yield in area. Rainwater harvesting recommended."})
    else:
        alerts.append({"type": "water_scarcity", "severity": "Low", "icon": "✅", "color": "green",
                        "title": "Adequate Water Supply",
                        "detail": f"Water scarcity score: {water_score}/100. Area generally has adequate water resources.",
                        "recommendation": "Standard checks sufficient. Verify municipal water connection availability."})

    # ── 3. Illegal Layout / Unauthorized Colony ──
    illegal_data = _ILLEGAL_LAYOUT_RISK.get(city_state, None)
    if illegal_data:
        il_score = illegal_data["score"]
        alerts.append({"type": "illegal_layout", "severity": "High" if il_score >= 60 else "Moderate", "icon": "🚨" if il_score >= 60 else "⚠️", "color": "red" if il_score >= 60 else "orange",
                        "title": f"Illegal Layout Risk – {illegal_data['reported_cases']} Reports",
                        "detail": f"Illegal layout risk score: {il_score}/100. {illegal_data['details']}",
                        "recommendation": "ALWAYS verify layout approval from the local planning authority (DTCP/DA/HMDA etc.) before purchase. Check RERA registration."})
    else:
        il_score = max(15, 50 - infra_score // 2)
        alerts.append({"type": "illegal_layout", "severity": "Low", "icon": "✅", "color": "green",
                        "title": "No Major Illegal Layout Reports",
                        "detail": f"No widespread illegal layout issues reported for this specific city (score: {il_score}/100). However, always verify layout approval.",
                        "recommendation": "Still verify layout/plot approval from local development authority as a standard practice."})
    risk_scores["illegal_layout"] = illegal_data["score"] if illegal_data else il_score

    # ── 4. Land Dispute History ──
    dispute_data = _LAND_DISPUTE_HISTORY.get(city_state, None)
    if dispute_data:
        ld_score = dispute_data["score"]
        alerts.append({"type": "land_dispute", "severity": "High" if ld_score >= 60 else "Moderate", "icon": "⚖️", "color": "red" if ld_score >= 60 else "orange",
                        "title": f"Land Dispute History – {dispute_data['dispute_type']}",
                        "detail": f"Dispute risk score: {ld_score}/100. {dispute_data['details']}",
                        "recommendation": "Conduct thorough title search (30+ years). Check local court records. Hire a local property lawyer."})
    else:
        ld_score = max(10, 40 - infra_score // 3)
        alerts.append({"type": "land_dispute", "severity": "Low", "icon": "✅", "color": "green",
                        "title": "No Major Dispute History on Record",
                        "detail": f"No widespread land disputes documented for this city (score: {ld_score}/100).",
                        "recommendation": "Standard title verification and EC check is still recommended."})
    risk_scores["land_dispute"] = dispute_data["score"] if dispute_data else ld_score

    # ── 5. Distance from Development Zones ──
    dev_distance_score = _ZONE_DEV_DISTANCE.get(zone_type, 30)
    risk_scores["dev_distance"] = dev_distance_score

    if dev_distance_score <= 10:
        alerts.append({"type": "dev_distance", "severity": "Low", "icon": "🏙️", "color": "green",
                        "title": "Within or Adjacent to Development Zone",
                        "detail": f"Development distance score: {dev_distance_score}/100 (lower = closer). This is a core development zone ({zone_type}). Major infrastructure, commercial hubs, and employment centres are nearby.",
                        "recommendation": "Prime location. Focus on micro-locality checks (traffic, noise, specific neighbourhood)."})
    elif dev_distance_score <= 20:
        alerts.append({"type": "dev_distance", "severity": "Low-Moderate", "icon": "🔄", "color": "blue",
                        "title": "Near Development Zone – Growth Corridor",
                        "detail": f"Development distance score: {dev_distance_score}/100. Located in expanding development belt ({zone_type}). Infrastructure improving.",
                        "recommendation": "Good growth potential. Verify upcoming infrastructure projects (metro, highway, SEZ) in master plan."})
    elif dev_distance_score <= 30:
        alerts.append({"type": "dev_distance", "severity": "Moderate", "icon": "📍", "color": "orange",
                        "title": "Moderate Distance from Major Development",
                        "detail": f"Development distance score: {dev_distance_score}/100. Zone type: {zone_type}. Not in immediate development corridor but may benefit from planned expansion.",
                        "recommendation": "Check city master plan for future zoning. Verify road connectivity and upcoming projects."})
    else:
        alerts.append({"type": "dev_distance", "severity": "High", "icon": "🏔️", "color": "red",
                        "title": "Far from Major Development Zones",
                        "detail": f"Development distance score: {dev_distance_score}/100. Zone type: {zone_type}. Area is relatively remote from IT/industrial/commercial hubs. Appreciation may be slower.",
                        "recommendation": "Suitable for specific purposes (tourism, retirement, agriculture). Not ideal for quick investment returns. Verify basic amenities access."})

    # ── Overall Area Risk Score ──
    weights = {"flood": 0.25, "water_scarcity": 0.2, "illegal_layout": 0.25, "land_dispute": 0.2, "dev_distance": 0.1}
    overall = sum(risk_scores[k] * weights[k] for k in weights)

    if overall >= 65:
        overall_label = "🔴 High Area Risk"
    elif overall >= 45:
        overall_label = "🟠 Moderate Area Risk"
    elif overall >= 30:
        overall_label = "🟡 Low-Moderate Risk"
    else:
        overall_label = "🟢 Low Area Risk"

    return {
        "alerts": alerts,
        "risk_scores": risk_scores,
        "overall_score": round(overall, 1),
        "overall_label": overall_label,
    }
