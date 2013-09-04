#!/usr/bin/env python

c = 612
d = {
  # date        rr  qq
  "2013-05-04": [1, 1.3],      # 6
  "2013-05-05": [0, 1.3],      # 7
  "2013-05-06": [0, 1.3],      # 1 
  "2013-05-07": [0, 0.5],      # 2
  "2013-05-08": [0.2, 1.0],    # 3
  "2013-05-09": [0.2, 1.3],    # 4
  "2013-05-10": [0.5, 1.3],    # 5
  "2013-05-11": [0.2, 0.5],    # 6
  "2013-05-12": [0.4, 1.3],    # 7
  "2013-05-13": [0.1, 1.3],    # 1
  "2013-05-14": [0.2, 1.3],    # 2
  "2013-05-15": [0, 1.3],      # 3
  "2013-05-16": [0.01, 1.0],   # 4
  "2013-05-17": [0, 0],        # 5
  "2013-05-18": [0.01, 1.0],   # 6
  "2013-05-19": [0, 0.5],      # 7
  "2013-05-20": [0.2, 1.0],    # 1
  "2013-05-21": [0.3, 1.0],    # 2
  "2013-05-22": [0.1, 1.3],    # 3
  "2013-05-23": [0, 1.3],      # 4
  "2013-05-24": [0.1, 1.3],    # 5
  "2013-05-25": [0.3, 1.3],    # 6
  "2013-05-26": [0.1, 1.3],    # 7    05-27 0:00
  "2013-05-27": [0, 1],        # 1
  "2013-05-28": [0.1, 0.5],    # 2    05-29 0:28
  "2013-05-29": [0.1, 1],      # 3       # qq 修改策略，每天最多1天.
  "2013-05-30": [0.3, 1],      # 4    
  "2013-05-31": [0.3, 1],      # 5
  "2013-06-01": [0, 1],        # 6   06-02 0:10
  "2013-06-02": [0, 1],        # 7   06-03 0:15
  "2013-06-03": [0.4, 1],      # 1   06-04 0:08
  "2013-06-04": [0.2, 1],      # 2   她说半年不再去xiaonei网了
  "2013-06-05": [0, 1],        # 3
  "2013-06-06": [0, 1],        # 4
  "2013-06-07": [0, 1],        # 5
  "2013-06-08": [0.01, 1],     # 6   06-08 18:27
  "2013-06-09": [0, 1],        # 7
  "2013-06-10": [0, 1],        # 1   06-10 22:28
  "2013-06-11": [0, 1],        # 2   
  "2013-06-12": [0, 1],        # 3   06-12 20:00
  "2013-06-13": [0, 1],        # 4   
  "2013-06-14": [0, 1],        # 5
  "2013-06-15": [0, 0.5],      # 6   06-15 10:18
  "2013-06-16": [0, 1],        # 7
  "2013-06-17": [0, 1],        # 1   06-17 22:46
  "2013-06-18": [0, 1],        # 2   
  "2013-06-19": [0, 0.5],      # 3
  "2013-06-20": [0, 0.5],      # 4  
  "2013-06-21": [0, 0.5],      # 5
  "2013-06-23": [0, 0.5],      # 7
  "2013-06-24": [0, 0.5],      # 1
  "2013-06-25": [0, 1],        # 2   耳机是风的天线。。。
  "2013-06-26": [0, 1.3],      # 3   
  "2013-06-27": [0, 0.3],      # 4  
  "2013-06-28": [0, 1.3],      # 5   06-28 15:48
  "2013-06-29": [0, 0.8],      # 6 
  "2013-06-30": [0, 1.0],      # 7
  "2013-07-01": [0, 1.0],      # 1
  "2013-07-02": [0, 1.0],      # 2
  "2013-07-03": [0, 1.0],      # 3   房子在地上，树在天上。结果他们把房子种在了天上，又把树埋到了地里。
  "2013-07-04": [0, 1.0],      # 4
  "2013-07-05": [0, 1.0],      # 5
  "2013-07-06": [0, 1.0],      # 6
  "2013-07-07": [0, 1.0],      # 7
  "2013-07-08": [0, 1.0],      # 1
  "2013-07-09": [0, 1.0],      # 2
  "2013-07-10": [0, 1.0],      # 3
  "2013-07-11": [0, 0.5],      # 4
  "2013-07-12": [0, 1.0],      # 5
  "2013-07-13": [0, 0.5],      # 6
   #
  "2013-07-15": [0, 0.5],      # 1
  "2013-07-16": [0, 1],
  "2013-07-17": [0, 1],
  "2013-07-18": [0, 0.5],      # 4
  "2013-07-19": [0, 1],        # 5
  "2013-07-20": [0, 1],        # 6
  "2013-07-21": [0, 1],        # 7  07-21 23:15
  "2013-07-22": [0, 1],        # 1  07-22 23:14
  "2013-07-23": [0, 1],        # 2  07-23 23:14
  "2013-07-24": [0, 1],        # 3  
  "2013-07-25": [0, 1],        # 4  07-26 02:04  我的qq被盗了?
  "2013-07-26": [0, 1],        # 5  07-27 00:25  我越来越觉得香川好帅啊。。。难道是被烘托出来的
  "2013-07-27": [0, 1],        # 6
  "2013-07-28": [0, 1],        # 7  07-28 23:37
  "2013-07-29": [0, 1],        # 1  07-30 01:27
  "2013-07-30": [0, 1],        # 2  07-31 01:17
  "2013-07-31": [0, 1],
  "2013-08-01": [0, 1],       
  "2013-08-02": [0, 1],
  "2013-08-03": [0, 0.5],      #   08-04 01:09
  "2013-08-04": [0, 1],       
  "2013-08-05": [0, 1],   
  "2013-08-06": [0, 0.5],      # 对家里的高温严重估计不足
  "2013-08-07": [0, 1],
  "2013-08-08": [0, 0.5],
  "2013-08-09": [0, 0.5],      #  08-09 15:55
  "2013-08-10": [0, 1.0],      #  08-10 17:22
  "2013-08-11": [0, 0.5],
  "2013-08-12": [0, 1.0],      # (qq签名没有了)
  "2013-08-13": [0, 0.5],      # 手机丢了，不要被骗，包括邮箱和微信和qq
                               # 08-13 21:22
  "2013-08-14": [0, 1],   
  "2013-08-15": [0, 0.5],    #
  "2013-08-16": [0, 0.5], 
  "2013-08-17": [0, 1], 
  "2013-08-18": [0, 1.3],    #  （qq 签名没有了)
  "2013-08-19": [0, 1.3],
  "2013-08-20": [0, 1.3],   
  "2013-08-21": [0, 1.3], 
  "2013-08-22": [0, 1.3],
  "2013-08-23": [0, 1.3],
  "2013-08-24": [0, 0.8],
  "2013-08-25": [0, 1.3],
  "2013-08-26": [0, 1.3],
  "2013-08-27": [0, 1.3],
  "2013-08-28": [0, 1.3],    # 08-29 10:25
  "2013-08-29": [0, 1.3],    # 08-30 11:46
  "2013-08-30": [0, 1.3],
  "2013-08-31": [0, 1.3],
  "2013-09-01": [0, 1.3],
  "2013-09-02": [0, 1.3],    # 我还总嘲笑阿森纳屌丝。。。结果人家留了张大王抄底。。。
  "2013-09-03": [0, 1.3],    # 09-03 20:03
  "2013-09-04": [0, 1.3],    # 09-04 23:35
}

