# IHT-based-public-auditing-for-cloud-storage
Ｕsing Index Hash Table,　A public auditing scheme checks the verification for cloud storage, particularly dynamic data.

The protocol for public auditing is implemented on top of Cryptography (PBC) library. Since I choosed the programming language, python,  to implement some algrithms in the protocol, I installed the charm-crypto 0.43 library on a linux system (ubuntu 16.04). You can find the charm-crypyto library here:https://pypi.python.org/pypi?%3Aaction=search&term=charm+crypto&submit=search

The structure of project file :
+----head.py

 ----myToolBox.py
 
 ----zhuScheme.py
 
 ----test0 ( not provided, you need to create the file)

Note: 
(1) The file for testing the algrithms is not provided and its path and name (test0) is used in the algrithms, so please create the file in your projects and change the file path in the funtions('TagGen' and 'Proof') when you run the programs.
(2) the paper 'p1550-zhu.pdf' describle the protocol in detail.
