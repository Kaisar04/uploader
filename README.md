# uploader
aws s3 uploader


config = TransferConfig(...) - конфигурация отвечает за многокомпонентную загрузку с несколькими потоками.
multipart_threshold - атрибут задает максимальный размер части файли при котором отработает многопоточность.
max_concurrency - атрибут задает количество потоков. Количество потоков по умолчанию - 10. Задаем на основе мощностей машины. 
multipart_chunksize - атрибут задает размер частей файлов (chunk)

Reference:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html