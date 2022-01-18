# Getting started with Darcy AI

The Darcy AI SDK offers a rich set of features that Darcy AI application developers can use to easily build complex AI processing chains. This makes developing rich real-time applications possible in a shorter timeframe and with a much more standardized approach.

If you have not yet read the overview of Darcy AI terminology, it is recommended that you do that first. You can find it here [Darcy AI Terminology Guide](./TERMINOLOGY.md)

## Thinking in terms of Darcy AI pipelines

The concept of an AI pipeline is similar to complex event processing (CEP) and data stream processing, but there are some unique aspects you will notice when building with the Darcy AI.

You are allowed only one Darcy AI pipeline in your application. There is a reason for this. A pipeline allows you to order the AI operations in a way that produces predictable trade-offs. One example is placing two different AI operations in parallel. On a hardware system that does not have enough AI accelerator hardware, Darcy will need to make a decision about how to run those operations. If you had more than one pipeline, Darcy would have conflicting intelligence about how to sequence the operations and you would be unable to predict which pipeline would be able to process.

You should consider a pipeline to be the backbone of your application flow. You only want one backbone and it should include all of the AI processing that you need in order to make your application run smoothly.

The way you structure the pipeline will have an effect on AI processing speed and timing reliability. For processes that must occur in a straight line, attach processing steps called Perceptors one after the other. For processes that can take place in any order and do not depend on one another, you can use parallel ordering.

A Darcy AI pipeline is a data graph and can be modeled visually like a sequence tree.
```
         p1 (0)        p2 (1)     p3 (1)
         /  \            |          |
    p11 (0) p12 (1)    p21 (0)    p31 (1)
               |
            p121 (1)
```