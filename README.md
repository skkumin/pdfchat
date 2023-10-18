# PDF Chat - How it work
<p align="center">
<img src="https://github.com/skkumin/pdfchat/assets/98961173/92a4d682-c22b-485d-a427-caa72fb08824">
</p>

### 프로젝트 소개
2023년 ChatGPT의 발표로 LLM의 엄청난 성능을 보여주었다.ChatGPT와 같은 LLM은 pretrain, fine tunning, RLHF(Reinforcement Learning with Human Feedback) 3개의 학습 단계를 거치는데 특히 이 첫번째 pretrain 단계에는 천문학 적인 비용이 들어간다.  
Hallucination(환각)은 이런 LLM의 제일 큰 단점으로 이는 pretrain과정에서 학습되지 않은 데이터에 대한 input으로 생기는 현상이다. 시간이 지날수록 text데이터의 생성 속도는 빨라지고 그 양 또한 많아지기 때문에 그 데이터를 계속 수집해 주기적으로 학습시키는것은 불가능하다(pretrain의 비용을 생각해봐도 불가능에 가깝다).  
그래서 이러한 Hallucination의 방지를 위해 RAG(Retreival Augmented Generation)을 사용할 수 있으며 ChatPDF는 RAG를 사용하는 대표적인 어플리케이션이다.  
따라서 해당 프로젝트를 통해 Chat pdf의 작동원리를 학습하고 openai의 api를 이용해 직접 어플리케이션을 제작해보았다.  

### 📂 DEMO

openai의 gpt-3.5-turbo API를 이용해 직접 PDF Chat을 구현한 데모로 기존 서비스 중인[PDF chat](https://www.chatpdf.com/?via=rickt1)의 기능에 추가적으로 2개의 PDF를 선택해 채팅할 수 있도록 데모를 제작하였으며 그 작동원리는 아래 [Muti PDF chat]을 통해 확인할 수 있다.
해당 작동원리에 대한 자세한 설명은 📂프로젝트상세/Demo.pdf에서 확인할 수 있다.

<p align="center">
<img src="https://github.com/skkumin/pdfchat/assets/98961173/4e253ba2-112e-421f-a7dc-dce5279ddc7e">
</p>
<p align="center">
[PDF chat]
</p>
<p align="center">
<img src="https://github.com/skkumin/pdfchat/assets/98961173/03c2eb3b-a761-4358-bb92-6b6b6b37a633">
</p>
<p align="center">
[Muti PDF chat]
</p>

### 📂 fine tunning

openai의 gpt-3.5-turbo API 사용 부분을 한국어 오픈소스 모델인 polyglot-ko를 이용하기위해 [context, question, answer]형식의 데이터셋을 만들고 QLora를 이용한 fine tunning을 진행하였다.  
데이터셋은 AI Hub에서 제공하는 MRC Dataset(기계 독해 데이터셋)을 사용하였고 해당 데이터로부터 [context, question, answer]의 Data를 가져왔다.  
가져온 데이터는 answer가 단답식으로 되있어 아래의 Prompt와 [context, question, answer]로 새로운 answer를 만들었다.  
gpt-3.5-tubo를 이용하여 만들었으며 정답 있는 데이터셋 9909개, 정답 없는 데이터셋 2000개를 만들었고 대략 $20 정도의 API 비용이 소모되었다.  
<p align="center">
<img src="https://github.com/skkumin/pdfchat/assets/98961173/87e3065f-2f67-4659-bef5-b20f14e460dd">
</p>
<p align="center">
<img src="https://github.com/skkumin/pdfchat/assets/98961173/7ae8fa9c-7260-4459-a020-b8e0b63b99b2">
</p>


