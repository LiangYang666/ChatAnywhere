# Chat-Anywhere

## Star the [Repository](https://github.com/LiangYang666/ChatAnywhere)  
## 特性
> 在任意软件内使用  
> 编写文档的好助手  

## 演示动图
选中文本作为上下文提示，按下快捷键`Ctrl+Alt+\`激活补全
![演示](https://user-images.githubusercontent.com/38237931/230561942-a58766e4-6806-4b79-a304-5f690b49d7bb.gif)


## 设置界面
![image](https://user-images.githubusercontent.com/38237931/230561900-6dc6a49a-cf7e-4007-a296-9b12341d4bf1.png)


## 使用前提（目前仅支持Windows）
> 1. 因国内IP被封或OpenAI API被墙，因此自己需要有代理，稍后需要配置  
> 2. 有openai账号，注册事项可以参考[此文章](https://juejin.cn/post/7173447848292253704)   
> 3. 创建好api_key, 进入[OpenAI链接](https://platform.openai.com/),右上角点击，进入页面设置  
![image](https://user-images.githubusercontent.com/38237931/222461544-260ef350-2d05-486d-bf36-d078873b0f7a.png)

## 部署方法
> 1. 执行 `pip install -r requirements.txt`安装必要包  
> 2. 执行`OPANAI_API_KEY=sk-XXXX python main.py`来运行，其中`sk-XXXX`为你的apikey  
> 3. 在弹出的界面中配置代理或apikey， 上面已有默认配置，也可打开`main.py`文件，在程序中修改API_KEY和https_proxy默认值  
> 4. 关于更新，当代码更新时，使用git pull更新重新部署即可 



