# PDF Chat - How it work
<p align="center">
<img src="https://github.com/skkumin/pdfchat/assets/98961173/92a4d682-c22b-485d-a427-caa72fb08824">
</p>

### 프로젝트 소개
2023년 ChatGPT의 발표로 LLM의 엄청난 성능을 보여주었다.ChatGPT와 같은 LLM은 pretrain, fine tunning, RLHF(Reinforcement Learning with Human Feedback) 3개의 학습 단계를 거치는데 특히 이 첫번째 pretrain 단계에는 천문학 적인 비용이 들어간다.
Hallucination(환각)은 이런 LLM의 제일 큰 단점으로 이는 pretrain과정에서 학습되지 않은 데이터에 대한 input으로 생기는 현상이다. 시간이 지날수록 text데이터의 생성 속도는 빨라지고 그 양 또한 많아지기 때문에 그 데이터를 계속 수집해 주기적으로 학습시키는것은 불가능하다(pretrain의 비용을 생각해봐도 불가능에 가깝다).
그래서 이러한 Hallucination의 방지를 위해 RAG(Retreival Augmented Generation)을 사용할 수 있으며 ChatPDF는 RAG를 사용하는 대표적인 어플리케이션이다.
따라서 해당 프로젝트를 통해 Chat pdf의 작동원리를 학습하고 openai의 api를 이용해 직접 어플리케이션을 제작해보았다.
