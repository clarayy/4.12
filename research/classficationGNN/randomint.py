import random
#随机生成0-217之间的数，用来打乱生成数据的顺序
# nodelist=[]
# for i in range(217):
#     a = random.randint(0,216)
#     nodelist.append(a)
#     #print(a)
# print('nodelist = ',nodelist)
# print(nodelist[:100],len(nodelist[:100]))
# print(nodelist[100:400],len(nodelist[100:400]))
# print(nodelist[400:],len(nodelist[400:]))
#
#第一级分类的classlabel，0-99对应1,100-199对应2等
# node = [0,100,200,300,400,99,199,299,399,499]
# for i in node:
#     print(i//100)
#
#wiki800个#nodelist =  [219, 686, 234, 667, 640, 233, 303, 578, 44, 427, 645, 331, 588, 122, 78, 112, 656, 599, 1, 531, 674, 31, 98, 383, 609, 319, 47, 278, 503, 648, 441, 372, 573, 468, 602, 93, 466, 264, 110, 465, 40, 129, 545, 187, 437, 428, 175, 517, 624, 274, 612, 483, 591, 362, 626, 543, 587, 81, 481, 67, 679, 411, 278, 44, 599, 232, 431, 72, 451, 658, 177, 209, 694, 445, 542, 429, 309, 302, 680, 690, 621, 227, 410, 177, 690, 133, 179, 456, 625, 559, 648, 81, 353, 182, 297, 1, 356, 555, 330, 598, 509, 445, 346, 680, 679, 27, 206, 120, 345, 574, 168, 506, 539, 525, 502, 670, 688, 171, 64, 668, 182, 652, 324, 97, 114, 412, 269, 246, 395, 421, 608, 432, 497, 617, 270, 192, 172, 394, 458, 619, 561, 507, 432, 233, 148, 233, 175, 421, 643, 657, 125, 602, 255, 284, 453, 596, 442, 143, 417, 224, 2, 281, 59, 622, 639, 674, 74, 637, 203, 609, 173, 23, 213, 282, 62, 356, 355, 513, 112, 76, 525, 118, 479, 573, 113, 315, 610, 375, 372, 482, 25, 670, 619, 277, 294, 527, 503, 549, 2, 102, 296, 98, 508, 20, 112, 510, 427, 549, 292, 620, 129, 154, 219, 515, 589, 126, 685, 167, 528, 312, 628, 397, 73, 426, 294, 662, 271, 266, 206, 351, 503, 481, 305, 582, 306, 55, 387, 332, 398, 53, 560, 213, 503, 370, 602, 542, 399, 128, 429, 366, 20, 226, 625, 62, 374, 242, 382, 509, 276, 335, 522, 613, 610, 550, 419, 384, 604, 206, 349, 340, 629, 632, 123, 611, 401, 74, 513, 527, 500, 683, 144, 191, 448, 251, 570, 97, 609, 62, 446, 628, 484, 97, 427, 175, 679, 23, 680, 39, 214, 642, 466, 147, 43, 274, 427, 171, 103, 456, 24, 6, 572, 555, 34, 94, 148, 596, 41, 20, 35, 87, 506, 285, 403, 224, 377, 314, 179, 695, 622, 379, 356, 639, 567, 447, 675, 301, 202, 168, 637, 458, 512, 382, 477, 441, 302, 699, 427, 32, 198, 528, 632, 678, 170, 302, 211, 388, 261, 663, 273, 213, 89, 437, 301, 395, 543, 154, 675, 357, 52, 451, 437, 541, 491, 300, 296, 457, 456, 404, 309, 159, 422, 50, 67, 493, 517, 363, 349, 607, 212, 541, 502, 604, 468, 458, 65, 533, 88, 366, 549, 64, 688, 434, 48, 556, 194, 481, 492, 208, 573, 79, 229, 450, 660, 249, 394, 27, 588, 505, 81, 456, 155, 510, 362, 302, 52, 453, 434, 506, 127, 347, 547, 232, 80, 345, 119, 584, 217, 133, 28, 285, 596, 385, 532, 582, 93, 130, 199, 25, 671, 233, 401, 322, 411, 519, 67, 595, 301, 229, 157, 129, 697, 583, 105, 453, 37, 291, 358, 635, 14, 481, 618, 436, 605, 610, 126, 241, 369, 428, 87, 377, 632, 695, 367, 211, 331, 554, 682, 169, 667, 413, 683, 37, 439, 690, 157, 391, 216, 559, 36, 336, 699, 147, 483, 87, 173, 533, 179, 456, 469, 78, 141, 108, 349, 197, 95, 178, 85, 450, 267, 350, 207, 91, 299, 240, 574, 230, 24, 475, 639, 149, 550, 464, 414, 99, 448, 224, 505, 254, 195, 132, 457, 655, 134, 382, 166, 433, 171, 417, 426, 538, 621, 324, 577, 363, 54, 545, 367, 600, 399, 585, 210, 211, 52, 354, 483, 430, 13, 294, 660, 582, 82, 677, 552, 56, 153, 403, 109, 191, 649, 397, 158, 406, 239, 284, 296, 526, 352, 267, 284, 204, 258, 600, 226, 348, 13, 400, 653, 622, 485, 631, 220, 260, 90, 58, 506, 571, 425, 379, 334, 669, 96, 111, 508, 341, 338, 626, 413, 580, 610, 377, 642, 397, 449, 392, 161, 647, 634, 389, 327, 219, 211, 617, 267, 411, 258, 363, 554, 531, 180, 67, 29, 165, 65, 573, 360, 27, 681, 349, 450, 342, 591, 293, 72, 438, 555, 392, 259, 412, 257, 40, 631, 498, 230, 558, 456, 479, 281, 507, 558, 579, 540, 436, 695, 332, 252, 283, 413, 399, 344, 599, 244, 56, 500, 518, 340, 437, 273, 192, 449, 143, 320, 662, 696, 24, 98, 338, 439, 415, 344, 295]
#randint1000个#nodelist =  [847, 94, 934, 259, 67, 702, 316, 404, 98, 75, 999, 892, 921, 791, 347, 998, 869, 729, 162, 17, 882, 617, 523, 723, 532, 902, 801, 620, 634, 147, 662, 
# 168, 192, 45, 947, 667, 134, 104, 606, 648, 587, 943, 844, 128, 929, 888, 725, 246, 6, 521, 545, 910, 866, 483, 46, 89, 473, 534, 991, 502, 258, 264, 955, 362,
#  601, 292, 326, 329, 271, 872, 816, 774, 46, 561, 237, 839, 8, 953, 646, 603, 779, 10, 289, 931, 155, 361, 246, 529, 714, 433, 154, 84, 693, 410, 769, 791, 646, 
# 811, 867, 829, 371, 266, 338, 249, 676, 543, 897, 277, 228, 860, 70, 222, 344, 183, 559, 711, 802, 775, 343, 196, 346, 231, 860, 213, 104, 643, 279, 377, 
# 106, 995, 730, 253, 313, 198, 403, 473, 652, 620, 161, 324, 846, 855, 10, 476, 519, 166, 896, 852, 543, 338, 904, 913, 911, 773, 78, 75, 293, 387, 636, 575, 
# 683, 847, 999, 993, 441, 994, 338, 818, 239, 441, 685, 1, 406, 467, 430, 668, 846, 347, 729, 156, 952, 948, 648, 245, 202, 313, 577, 745, 600, 559, 343, 
# 485, 254, 300, 97, 566, 116, 25, 628, 61, 617, 820, 374, 672, 958, 109, 299, 509, 247, 137, 113, 725, 271, 730, 843, 666, 383, 987, 782, 994, 977, 156, 644, 
# 848, 23, 160, 574, 531, 929, 370, 341, 219, 883, 939, 870, 109, 977, 934, 508, 162, 340, 667, 227, 987, 841, 921, 539, 579, 719, 395, 621, 164, 241, 171, 99,
#  296, 729, 53, 140, 596, 247, 953, 529, 656, 627, 159, 280, 551, 947, 555, 621, 690, 301, 714, 924, 601, 831, 461, 157, 666, 547, 227, 331, 722, 325, 291, 129, 
# 834, 827, 145, 980, 94, 328, 672, 36, 716, 824, 667, 583, 547, 155, 545, 32, 576, 877, 288, 266, 124, 200, 460, 583, 979, 607, 842, 741, 965, 103, 836, 994, 
# 422, 535, 759, 128, 404, 331, 16, 753, 999, 75, 112, 476, 303, 556, 366, 406, 756, 117, 710, 605, 858, 7, 828, 351, 751, 874, 307, 194, 683, 443, 317, 579, 
# 883, 871, 866, 594, 769, 120, 35, 638, 786, 313, 570, 554, 841, 430, 671, 149, 960, 286, 976, 754, 739, 875, 849, 704, 923, 623, 914, 195, 390, 586, 421, 
# 365, 963, 11, 577, 836, 678, 345, 517, 636, 761, 773, 920, 86, 357, 15, 126, 94, 862, 168, 315, 30, 849, 343, 122, 332, 224, 849, 883, 871, 469, 856, 336, 
# 988, 333, 606, 515, 67, 283, 207, 510, 87, 486, 363, 291, 233, 417, 270, 793, 903, 346, 581, 7, 651, 236, 631, 536, 430, 233, 506, 132, 743, 228, 788, 596, 
# 597, 459, 339, 167, 743, 982, 507, 406, 730, 484, 902, 688, 40, 172, 198, 233, 719, 535, 607, 475, 724, 959, 158, 553, 977, 529, 130, 910, 185, 684, 502, 
# 460, 912, 370, 498, 713, 352, 913, 137, 664, 639, 590, 388, 568, 754, 450, 299, 441, 951, 550, 240, 330, 385, 713, 158, 798, 83, 188, 444, 384, 472, 394, 
# 389, 897, 874, 294, 222, 841, 240, 854, 831, 729, 491, 176, 734, 805, 11, 512, 609, 259, 968, 750, 397, 448, 164, 910, 304, 762, 783, 793, 842, 379, 700, 
# 884, 368, 679, 88, 306, 398, 124, 224, 167, 502, 195, 472, 249, 200, 377, 174, 782, 978, 90, 556, 957, 484, 269, 653, 355, 231, 813, 687, 188, 529, 654,
#  875, 846, 167, 890, 958, 846, 1000, 741, 574, 189, 118, 401, 378, 530, 198, 61, 442, 220, 404, 945, 190, 659, 227, 129, 862, 354, 208, 914, 10, 290, 63,
#  783, 455, 682, 492, 832, 322, 412, 843, 101, 942, 569, 46, 173, 126, 940, 282, 364, 869, 554, 263, 842, 679, 256, 221, 256, 836, 355, 991, 98, 275, 738, 
# 238, 156, 771, 67, 966, 573, 426, 886, 41, 626, 217, 827, 450, 227, 782, 285, 285, 471, 324, 997, 592, 298, 383, 951, 953, 307, 154, 726, 127, 404, 850, 
# 641, 24, 133, 269, 657, 380, 423, 6, 19, 507, 634, 26, 471, 174, 385, 436, 488, 888, 702, 340, 443, 957, 851, 626, 39, 463, 727, 852, 366, 662, 782, 55, 888,
#  595, 500, 891, 224, 774, 232, 848, 27, 365, 607, 859, 810, 35, 697, 653, 482, 194, 962, 512, 20, 601, 801, 752, 192, 524, 208, 42, 307, 935, 225, 341, 141, 877, 
# 493, 977, 80, 784, 173, 182, 442, 414, 684, 686, 117, 763, 248, 158, 359, 863, 901, 305, 731, 338, 810, 204, 755, 100, 956, 504, 370, 33, 65, 934, 727, 38, 357, 
# 417, 693, 124, 455, 289, 330, 760, 752, 675, 648, 420, 703, 908, 817, 230, 995, 446, 466, 771, 179, 688, 66, 579, 231, 994, 525, 474, 623, 367, 707, 752, 267,
#  729, 51, 605, 278, 467, 646, 462, 17, 893, 470, 425, 676, 107, 564, 467, 485, 144, 563, 390, 33, 886, 22, 603, 978, 83, 13, 947, 967, 541, 187, 269, 584, 101,
#  298, 989, 205, 614, 926, 629, 168, 659, 29, 294, 91, 558, 276, 534, 393, 56, 456, 304, 342, 257, 464, 901, 696, 551, 297, 806, 879, 313, 997, 85, 514, 869,
#  417, 635, 378, 650, 361, 488, 929, 11, 535, 614, 733, 771, 236, 699, 275, 81, 980, 730, 630, 449, 8, 723, 899, 765, 585, 507, 844, 76, 648, 702, 400, 346, 
# 824, 866, 360, 175, 183, 325, 648, 507, 256, 261, 452, 426, 704, 116, 287, 42, 438, 398, 392, 335, 752, 200, 677, 478, 722, 144, 690, 785, 113, 274, 829, 
# 755, 51, 456, 426, 606, 201, 300, 824, 942, 680, 335, 976, 459, 569, 360, 796, 651, 404, 277, 947, 583, 573, 72, 166, 284, 984, 385, 746, 0, 582, 160, 445,
#  630, 908, 0, 700, 19, 543, 686, 989, 448, 581, 144, 425, 
# 410, 387, 561, 973, 969, 530, 605, 893, 649, 582, 57, 660, 914, 410, 579, 368, 938, 130, 606, 915, 803, 120, 928, 61, 708, 20, 975, 71, 163, 163, 693, 965, 735, 822]

# #randint500个数：
# nodelist =  [476, 469, 53, 457, 379, 159, 45, 236, 103, 315, 195, 455, 420, 341, 324, 229, 162, 407, 239, 159, 495, 176, 376, 231,
#      346, 257, 89, 113, 173, 134, 255, 30, 153, 378, 69, 433, 480, 94, 381, 405, 436, 22, 78, 244, 211, 76, 132, 67, 49, 283, 459, 209, 151, 349, 
#      179, 286, 378, 89, 210, 351, 14, 240, 361, 190, 217, 306, 221, 479, 322, 10, 484, 293, 304, 284, 440, 106, 125, 232, 420, 146, 364, 230,
#       359, 216, 327, 323, 299, 291, 73, 342, 49, 431, 280, 106, 477, 117, 77, 144, 225, 155, 330, 273, 204, 169, 113, 236, 176, 234, 461, 62,
#        392, 148, 177, 281, 224, 450, 408, 366, 214, 363, 403, 36, 125, 475, 115, 445, 437, 479, 93, 460, 234, 389, 458, 226, 118, 38, 466, 74, 
#        176, 361, 168, 193, 259, 402, 376, 459, 176, 404, 312, 115, 151, 117, 149, 454, 90, 443, 281, 3, 346, 106, 450, 453, 89, 398, 350, 101, 
#        316, 78, 216, 28, 186, 145, 334, 84, 432, 26, 212, 216, 411, 29, 457, 180, 208, 127, 344, 365, 436, 486, 258, 54, 352, 88, 250, 432, 
#        241, 476, 182, 42, 102, 291, 185, 360, 300, 224, 62, 93, 151, 394, 359, 131, 394, 96, 268, 210, 478, 193, 441, 2, 91, 197, 430, 497, 
#        122, 14, 106, 92, 17, 107, 360, 384, 49, 60, 174, 133, 105, 346, 388, 324, 122, 315, 360, 464, 39, 205, 395, 286, 71, 266, 194, 326, 416, 
#        17, 417, 400, 200, 168, 348, 341, 236, 458, 131, 350, 284, 418, 202, 123, 228, 350, 298, 124, 324, 464, 203, 35, 124, 160, 21, 16, 277, 310, 94, 126, 330, 98, 
#        293, 223, 313, 180, 91, 432, 379, 304, 266, 115, 227, 493, 494, 172, 47, 64, 486, 39, 328, 239, 248, 134, 266, 370, 1, 204, 455, 8, 76, 101, 49, 332, 130, 184, 
#        192, 303, 468, 7, 485, 115, 232, 432, 96, 406, 364, 290, 276, 348, 85, 178, 48, 235, 245, 77, 409, 239, 339, 28, 199, 132, 172, 21, 323, 196, 293, 45, 310, 168,
#         205, 153, 360, 87, 322, 413, 369, 172, 405, 409, 344, 336, 403, 165, 256, 186, 2, 183, 220, 433, 404, 364, 135, 319, 32, 431, 10, 164, 23, 176, 339, 301, 213, 
#         283, 465, 233, 336, 374, 204, 460, 489, 363, 128, 67, 379, 346, 236, 50, 389, 153, 161, 419, 416, 361, 181, 273, 498, 94, 201, 241, 140, 40, 372, 347, 340, 11,
#         164, 229, 324, 51, 4, 29, 239, 189, 337, 296, 238, 372, 110, 210, 230, 177, 160, 10, 488, 372, 10, 374, 200, 318, 473, 316, 387, 176, 167, 220, 281, 447, 131,
#          471, 104, 153, 107, 396, 232, 79, 321, 91, 227, 363, 65, 4, 118, 256, 303, 186, 429, 490, 55, 492, 483, 403, 306, 83, 482, 70, 200, 425, 158, 312, 381, 262, 237, 
#          188, 482, 118, 437, 361, 94, 14, 136, 145, 303, 497, 269, 295, 240, 28]
# print(nodelist[300:350])

#random217
#nodelist =  [112, 98, 55, 174, 146, 173, 189, 70, 136, 70, 94, 41, 89, 131, 103, 23, 98, 126, 80, 113, 36, 98, 162, 130, 124, 75, 94, 30, 107, 170, 102, 128, 77, 169, 119, 203, 140, 123, 206, 207, 66, 155, 95, 60, 104, 77, 198, 192, 198, 6, 201, 19, 85, 203, 123, 162, 174, 159, 52, 179, 84, 14, 92, 158, 174, 195, 19, 49, 135, 113, 198, 62, 24, 163, 76, 66, 139, 133, 45, 176, 158, 82, 197, 35, 83, 59, 2, 71, 169, 211, 16, 13, 5, 118, 26, 68, 168, 64, 208, 80, 122, 54, 71, 92, 189, 0, 110, 203, 142, 106, 92, 174, 3, 61, 68, 134, 36, 103, 162, 61, 82, 124, 151, 209, 147, 7, 16, 122, 125, 29, 143, 158, 187, 16, 126, 209, 8, 7, 164, 23, 20, 154, 74, 166, 116, 13, 100, 44, 131, 62, 46, 62, 137, 189, 55, 6, 164, 165, 24, 116, 210, 5, 119, 40, 156, 117, 135, 74, 1, 144, 199, 150, 110, 184, 19, 2, 146, 139, 146, 193, 211, 82, 205, 177, 21, 52, 211, 133, 48, 93, 202, 213, 149, 76, 148, 142, 148, 13, 97, 14, 50, 60, 54, 183, 210, 163, 195, 83, 55, 131, 87, 79, 56, 129, 14, 44, 119]

# #将100-199节点对应为0-99
# answer ={}
# a=0
# for i in range(100):
#     answer[a]=i
#     a=a+1
# print(answer)
#
# #第一级分类，用jordancenter来确定属于那一类，看准确率
# jordancenter = []
# file = '/home/iot/zcy/usb/copy/MINIST/MINIST/mydata/food500_SI_A5_m10_test/food500_SI_A5_m10_test_jordancenter.txt'
# with open(file,'r') as f:
#     for line in f.readlines():
#         line = line.strip('\n')
#         jordancenter .append(int(line))
# print(jordancenter)
# jc_class = []
# for i in jordancenter:
#     jc_class.append(i//100)
# labels = []
# file = '/home/iot/zcy/usb/copy/MINIST/MINIST/mydata/food500_SI_A5_m10_test/food500_SI_A5_m10_test_graph_labels.txt'
# with open(file,'r') as f:
#     for line in f.readlines():
#         line = line.strip('\n')
#         labels.append(int(line))
# print(labels)
# labels_class = []
# for i in labels:
#     labels_class.append(i//100)
# print(labels_class)
# count = 0
# for i in range(1000):
#     if jc_class[i]==labels_class[i]:
#         count=count+1
# print(count)
# labels = [[],[],[],[],[]]
# a=[2,1,3,4,5]
# for j in range(len(a)):
#     for i in range(5):
#         if a[j] == i:
#             labels[i].append(a[j])
# print(labels)
class0= {33: 0, 34: 1, 35: 2, 36: 3, 37: 4, 38: 5, 49: 6, 112: 7, 113: 8, 116: 9, 118: 10, 119: 11, 120: 12, 121: 13, 122: 14, 124: 15, 126: 16, 127: 17, 129: 18, 130: 19, 131: 20, 132: 21, 135: 22, 136: 23, 137: 24, 139: 25, 145: 26, 146: 27, 147: 28, 148: 29, 149: 30, 150: 31, 151: 32, 152: 33, 153: 34, 154: 35, 155: 36, 156: 37, 157: 38, 158: 39, 159: 40, 160: 41, 189: 42, 216: 43, 217: 44, 218: 45, 254: 46, 255: 47, 277: 48, 278: 49, 288: 50, 300: 51, 301: 52, 308: 53, 309: 54, 311: 55, 312: 56, 313: 57, 314: 58, 317: 59, 318: 60, 319: 61, 336: 62, 337: 63, 338: 64, 339: 65, 343: 66, 344: 67, 373: 68, 378: 69, 379: 70, 380: 71, 388: 72, 389: 73, 397: 74, 399: 75, 400: 76, 404: 77, 405: 78, 406: 79, 407: 80, 412: 81, 437: 82, 462: 83, 463: 84, 464: 85, 465: 86, 480: 87, 483: 88, 488: 89, 489: 90, 492: 91, 494: 92, 496: 93, 497: 94, 498: 95, 499: 96}
class1= {13: 0, 14: 1, 15: 2, 16: 3, 17: 4, 18: 5, 19: 6, 20: 7, 21: 8, 22: 9, 23: 10, 64: 11, 69: 12, 74: 13, 77: 14, 79: 15, 85: 16, 99: 17, 102: 18, 110: 19, 111: 20, 134: 21, 138: 22, 161: 23, 162: 24, 163: 25, 164: 26, 167: 27, 168: 28, 169: 29, 171: 30, 173: 31, 191: 32, 192: 33, 193: 34, 194: 35, 198: 36, 204: 37, 247: 38, 252: 39, 256: 40, 259: 41, 264: 42, 267: 43, 269: 44, 270: 45, 272: 46, 281: 47, 282: 48, 283: 49, 292: 50, 293: 51, 294: 52, 299: 53, 302: 54, 303: 55, 304: 56, 305: 57, 306: 58, 315: 59, 323: 60, 325: 61, 349: 62, 350: 63, 367: 64, 369: 65, 370: 66, 371: 67, 376: 68, 377: 69, 383: 70, 394: 71, 401: 72, 416: 73, 417: 74, 418: 75, 419: 76, 420: 77, 421: 78, 449: 79, 452: 80, 453: 81, 454: 82, 458: 83, 459: 84, 473: 85, 475: 86, 476: 87, 486: 88, 490: 89, 493: 90}
class2= {0: 0, 1: 1, 2: 2, 4: 3, 5: 4, 6: 5, 31: 6, 43: 7, 46: 8, 47: 9, 48: 10, 50: 11, 55: 12, 57: 13, 58: 14, 70: 15, 71: 16, 75: 17, 76: 18, 78: 19, 172: 20, 180: 21, 183: 22, 188: 23, 202: 24, 203: 25, 207: 26, 223: 27, 225: 28, 226: 29, 227: 30, 229: 31, 230: 32, 231: 33, 236: 34, 239: 35, 244: 36, 245: 37, 249: 38, 310: 39, 326: 40, 327: 41, 328: 42, 329: 43, 330: 44, 345: 45, 346: 46, 347: 47, 348: 48, 363: 49, 368: 50, 372: 51, 382: 52, 384: 53, 387: 54, 396: 55, 398: 56, 402: 57, 403: 58, 413: 59, 415: 60, 432: 61, 435: 62, 450: 63, 451: 64, 455: 65, 469: 66, 471: 67, 481: 68, 487: 69}
class3= {3: 0, 7: 1, 9: 2, 11: 3, 12: 4, 24: 5, 25: 6, 26: 7, 27: 8, 28: 9, 32: 10, 51: 11, 52: 12, 53: 13, 54: 14, 56: 15, 59: 16, 60: 17, 61: 18, 62: 19, 63: 20, 65: 21, 66: 22, 67: 23, 68: 24, 72: 25, 73: 26, 80: 27, 82: 28, 83: 29, 88: 30, 89: 31, 92: 32, 93: 33, 94: 34, 95: 35, 96: 36, 97: 37, 98: 38, 100: 39, 101: 40, 103: 41, 104: 42, 105: 43, 107: 44, 108: 45, 109: 46, 144: 47, 165: 48, 166: 49, 170: 50, 174: 51, 175: 52, 176: 53, 177: 54, 178: 55, 181: 56, 182: 57, 184: 58, 186: 59, 205: 60, 206: 61, 208: 62, 211: 63, 212: 64, 213: 65, 214: 66, 215: 67, 224: 68, 228: 69, 232: 70, 233: 71, 234: 72, 235: 73, 237: 74, 238: 75, 240: 76, 241: 77, 246: 78, 258: 79, 260: 80, 261: 81, 262: 82, 263: 83, 265: 84, 268: 85, 271: 86, 273: 87, 274: 88, 275: 89, 276: 90, 279: 91, 280: 92, 284: 93, 286: 94, 287: 95, 290: 96, 291: 97, 296: 98, 297: 99, 298: 100, 316: 101, 324: 102, 331: 103, 332: 104, 333: 105, 335: 106, 352: 107, 353: 108, 356: 109, 361: 110, 362: 111, 364: 112, 374: 113, 381: 114, 385: 115, 386: 116, 390: 117, 393: 118, 395: 119, 408: 120, 409: 121, 410: 122, 411: 123, 423: 124, 424: 125, 425: 126, 426: 127, 427: 128, 428: 129, 429: 130, 430: 131, 436: 132, 440: 133, 447: 134, 460: 135, 461: 136, 468: 137, 470: 138, 472: 139, 474: 140, 478: 141, 479: 142, 482: 143, 485: 144, 495: 145}
class4= {8: 0, 10: 1, 29: 2, 30: 3, 39: 4, 40: 5, 41: 6, 42: 7, 44: 8, 45: 9, 81: 10, 84: 11, 86: 12, 87: 13, 90: 14, 91: 15, 106: 16, 114: 17, 115: 18, 117: 19, 123: 20, 125: 21, 128: 22, 133: 23, 140: 24, 141: 25, 142: 26, 143: 27, 179: 28, 185: 29, 187: 30, 190: 31, 195: 32, 196: 33, 197: 34, 199: 35, 200: 36, 201: 37, 209: 38, 210: 39, 219: 40, 220: 41, 221: 42, 222: 43, 242: 44, 243: 45, 248: 46, 250: 47, 251: 48, 253: 49, 257: 50, 266: 51, 285: 52, 289: 53, 295: 54, 307: 55, 320: 56, 321: 57, 322: 58, 334: 59, 340: 60, 341: 61, 342: 62, 351: 63, 354: 64, 355: 65, 357: 66, 358: 67, 359: 68, 360: 69, 365: 70, 366: 71, 375: 72, 391: 73, 392: 74, 414: 75, 422: 76, 431: 77, 433: 78, 434: 79, 438: 80, 439: 81, 441: 82, 442: 83, 443: 84, 444: 85, 445: 86, 446: 87, 448: 88, 456: 89, 457: 90, 466: 91, 467: 92, 477: 93, 484: 94, 491: 95}

class_zong={33: 0, 34: 1, 35: 2, 36: 3, 37: 4, 38: 5, 49: 6, 112: 7, 113: 8, 116: 9, 118: 10, 119: 11, 120: 12, 121: 13, 122: 14, 124: 15, 126: 16, 127: 17, 129: 18, 130: 19, 131: 20, 132: 21, 135: 22, 136: 23, 137: 24, 139: 25, 145: 26, 146: 27, 147: 28, 148: 29, 149: 30, 150: 31, 151: 32, 152: 33, 153: 34, 154: 35, 155: 36, 156: 37, 157: 38, 158: 39, 159: 40, 160: 41, 189: 42, 216: 43, 217: 44, 218: 45, 254: 46, 255: 47, 277: 48, 278: 49, 288: 50, 300: 51, 301: 52, 308: 53, 309: 54, 311: 55, 312: 56, 313: 57, 314: 58, 317: 59, 318: 60, 319: 61, 336: 62, 337: 63, 338: 64, 339: 65, 343: 66, 344: 67, 373: 68, 378: 69, 379: 70, 380: 71, 388: 72, 389: 73, 397: 74, 399: 75, 400: 76, 404: 77, 405: 78, 406: 79, 407: 80, 412: 81, 437: 82, 462: 83, 463: 84, 464: 85, 465: 86, 480: 87, 483: 88, 488: 89, 489: 90, 492: 91, 494: 92, 496: 93, 497: 94, 498: 95, 499: 96,13: 0, 14: 1, 15: 2, 16: 3, 17: 4, 18: 5, 19: 6, 20: 7, 21: 8, 22: 9, 23: 10, 64: 11, 69: 12, 74: 13, 77: 14, 79: 15, 85: 16, 99: 17, 102: 18, 110: 19, 111: 20, 134: 21, 138: 22, 161: 23, 162: 24, 163: 25, 164: 26, 167: 27, 168: 28, 169: 29, 171: 30, 173: 31, 191: 32, 192: 33, 193: 34, 194: 35, 198: 36, 204: 37, 247: 38, 252: 39, 256: 40, 259: 41, 264: 42, 267: 43, 269: 44, 270: 45, 272: 46, 281: 47, 282: 48, 283: 49, 292: 50, 293: 51, 294: 52, 299: 53, 302: 54, 303: 55, 304: 56, 305: 57, 306: 58, 315: 59, 323: 60, 325: 61, 349: 62, 350: 63, 367: 64, 369: 65, 370: 66, 371: 67, 376: 68, 377: 69, 383: 70, 394: 71, 401: 72, 416: 73, 417: 74, 418: 75, 419: 76, 420: 77, 421: 78, 449: 79, 452: 80, 453: 81, 454: 82, 458: 83, 459: 84, 473: 85, 475: 86, 476: 87, 486: 88, 490: 89, 493: 90,0: 0, 1: 1, 2: 2, 4: 3, 5: 4, 6: 5, 31: 6, 43: 7, 46: 8, 47: 9, 48: 10, 50: 11, 55: 12, 57: 13, 58: 14, 70: 15, 71: 16, 75: 17, 76: 18, 78: 19, 172: 20, 180: 21, 183: 22, 188: 23, 202: 24, 203: 25, 207: 26, 223: 27, 225: 28, 226: 29, 227: 30, 229: 31, 230: 32, 231: 33, 236: 34, 239: 35, 244: 36, 245: 37, 249: 38, 310: 39, 326: 40, 327: 41, 328: 42, 329: 43, 330: 44, 345: 45, 346: 46, 347: 47, 348: 48, 363: 49, 368: 50, 372: 51, 382: 52, 384: 53, 387: 54, 396: 55, 398: 56, 402: 57, 403: 58, 413: 59, 415: 60, 432: 61, 435: 62, 450: 63, 451: 64, 455: 65, 469: 66, 471: 67, 481: 68, 487: 69,3: 0, 7: 1, 9: 2, 11: 3, 12: 4, 24: 5, 25: 6, 26: 7, 27: 8, 28: 9, 32: 10, 51: 11, 52: 12, 53: 13, 54: 14, 56: 15, 59: 16, 60: 17, 61: 18, 62: 19, 63: 20, 65: 21, 66: 22, 67: 23, 68: 24, 72: 25, 73: 26, 80: 27, 82: 28, 83: 29, 88: 30, 89: 31, 92: 32, 93: 33, 94: 34, 95: 35, 96: 36, 97: 37, 98: 38, 100: 39, 101: 40, 103: 41, 104: 42, 105: 43, 107: 44, 108: 45, 109: 46, 144: 47, 165: 48, 166: 49, 170: 50, 174: 51, 175: 52, 176: 53, 177: 54, 178: 55, 181: 56, 182: 57, 184: 58, 186: 59, 205: 60, 206: 61, 208: 62, 211: 63, 212: 64, 213: 65, 214: 66, 215: 67, 224: 68, 228: 69, 232: 70, 233: 71, 234: 72, 235: 73, 237: 74, 238: 75, 240: 76, 241: 77, 246: 78, 258: 79, 260: 80, 261: 81, 262: 82, 263: 83, 265: 84, 268: 85, 271: 86, 273: 87, 274: 88, 275: 89, 276: 90, 279: 91, 280: 92, 284: 93, 286: 94, 287: 95, 290: 96, 291: 97, 296: 98, 297: 99, 298: 100, 316: 101, 324: 102, 331: 103, 332: 104, 333: 105, 335: 106, 352: 107, 353: 108, 356: 109, 361: 110, 362: 111, 364: 112, 374: 113, 381: 114, 385: 115, 386: 116, 390: 117, 393: 118, 395: 119, 408: 120, 409: 121, 410: 122, 411: 123, 423: 124, 424: 125, 425: 126, 426: 127, 427: 128, 428: 129, 429: 130, 430: 131, 436: 132, 440: 133, 447: 134, 460: 135, 461: 136, 468: 137, 470: 138, 472: 139, 474: 140, 478: 141, 479: 142, 482: 143, 485: 144, 495: 145,8: 0, 10: 1, 29: 2, 30: 3, 39: 4, 40: 5, 41: 6, 42: 7, 44: 8, 45: 9, 81: 10, 84: 11, 86: 12, 87: 13, 90: 14, 91: 15, 106: 16, 114: 17, 115: 18, 117: 19, 123: 20, 125: 21, 128: 22, 133: 23, 140: 24, 141: 25, 142: 26, 143: 27, 179: 28, 185: 29, 187: 30, 190: 31, 195: 32, 196: 33, 197: 34, 199: 35, 200: 36, 201: 37, 209: 38, 210: 39, 219: 40, 220: 41, 221: 42, 222: 43, 242: 44, 243: 45, 248: 46, 250: 47, 251: 48, 253: 49, 257: 50, 266: 51, 285: 52, 289: 53, 295: 54, 307: 55, 320: 56, 321: 57, 322: 58, 334: 59, 340: 60, 341: 61, 342: 62, 351: 63, 354: 64, 355: 65, 357: 66, 358: 67, 359: 68, 360: 69, 365: 70, 366: 71, 375: 72, 391: 73, 392: 74, 414: 75, 422: 76, 431: 77, 433: 78, 434: 79, 438: 80, 439: 81, 441: 82, 442: 83, 443: 84, 444: 85, 445: 86, 446: 87, 448: 88, 456: 89, 457: 90, 466: 91, 467: 92, 477: 93, 484: 94, 491: 95}
class_zong
print(class_zong)