# Darcy AI SDK

This is the official software development kit (SDK) for building on the Darcy AI platform

## Introducing the Darcy AI platform

Darcy is an artificial intelligence (AI) that is focused on real-time interactions with the world around her. She has a variety of senses, such as vision and hearing, that allow her to perceive her environment. You can give Darcy additional senses, such as LiDAR or thermal vision, to expand her capabilities. Darcy is present in every device where a Darcy AI application is running. She runs entirely in each device. No data needs to leave the device and no computation is done in the cloud.

Darcy was designed to bring AI technology into the real world while keeping privacy and security as top priorities. Building real-time AI applications is very challenging. The Darcy AI SDK is a developer platform for computer vision and other applications which handles all of the most difficult and repetitive problems for you so you can focus on building amazing solutions.

With the Darcy AI SDK, you get everything you need to build real-time AI applications. If you can write web applications with Node.js or you have moderate Python experience, then you can develop a fully functioning AI app with Darcy. The SDK comes with documentation, build instructions, example applications, and more.

## How to use this SDK

The [docs](./docs) folder contains the full Darcy AI programming interface documentation and other helpful guide documents. Use this folder to learn about the Darcy AI platform and to get started. The guide documents will take you from an absolute beginner to building and deploying your own Darcy AI applications.

The [examples](./examples) folder contains a diverse set of sample applications that you can use as a reference or as a start of your own Darcy AI application. The code is commented to help you understand what to do and when to do it. The Darcy AI Explorer demo application is a rich and complex example that leverages nearly all of the programming interfaces that Darcy offers.

## What you need

You will need some hardware to run your Darcy AI application. Darcy can generally run on any device or computer with a Google Coral AI accelerator. Darcy AI applications are packaged into Docker containers, so the operating system can be Linux, Mac OS X, or Windows provided that the Docker container runtime is installed.

### System requirements

- ARM or x86 CPU (two or more cores recommended)
- Google Coral AI accelerator (more than one Coral increases performance for many applications)
- 512MB of RAM (4GB or more recommended)
- Camera (required for using Darcy with live video)
- Internet connectivity (wired Ethernet or WiFi)
- 200MB available disk space (1GB or more recommended and your application size will vary)
- Docker container runtime

### Darcy ready developer kits and edge boards

- Raspberry Pi with Coral USB
	- Raspberry Pi 4 single board computer [https://www.raspberrypi.com/products/raspberry-pi-4-model-b/](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
	- Google Coral AI accelerator USB module [https://coral.ai/products/accelerator/](https://coral.ai/products/accelerator/)
- Google Coral Dev Board [https://coral.ai/products/dev-board/](https://coral.ai/products/dev-board/)
- Google Coral Dev Board Mini [https://coral.ai/products/dev-board-mini/](https://coral.ai/products/dev-board-mini/)
- ASUS Tinker T [https://www.asus.com/us/Networking-IoT-Servers/AIoT-Industrial-Solutions/Tinker-Board-Series/Tinker-Edge-T/](https://www.asus.com/us/Networking-IoT-Servers/AIoT-Industrial-Solutions/Tinker-Board-Series/Tinker-Edge-T/)

## Getting started

If you haven't already become familiar with the Darcy AI platform terminology, check out this [Terminology Guide](./docs/TERMINOLOGY.md) to get up to speed quickly.

The best way to get started with Darcy is to see her in action. Start by trying out the Darcy AI Explorer application in the [Getting Started Guide](./docs/GETTINGSTARTED.md)

## Building

Learn how to package your Darcy AI application into a container that includes all of the dependencies needed to run with the [Build Guide](./docs/BUILD.md)

## Deploying

Learn how to deploy your Darcy AI application to your edge devices using the Edgeworx Cloud in the [Deployment Guide](./docs/DEPLOY.md)

## Documentation

Open the Darcy AI technical documentation to search and browse the API with code examples. This is a local documentation site that will run directly in your browser. The documentation is specific to each version of the Darcy AI SDK so it's the best place to reference when building. To open the documentation site locally use [Darcy AI Documentation Local Home Page](./docs/api/index.html)

If you prefer to access the latest Darcy AI developer documentation with an internet connection, use [Hosted Darcy AI Documentation](https://edgeworx.github.io/darcyai-engine/)

## Resources

### Getting help

- Get help from the other Darcy AI developers, the Darcy team, and the whole Darcy community on the Darcy AI Forum at [https://discuss.edgeworx.io/c/darcy-ai/](https://discuss.edgeworx.io/c/darcy-ai/)
- Report and track bugs in the Darcy AI platform and SDK using Github issues [https://github.com/edgeworx/darcyai-sdk/issues](https://github.com/edgeworx/darcyai-sdk/issues)

### Python packages for Darcy AI
- Darcy AI Engine package [https://pypi.org/project/darcyai-engine/](https://pypi.org/project/darcyai-engine/)
- Darcy AI Coral Accelerator extension package [https://pypi.org/project/darcyai-coral/](https://pypi.org/project/darcyai-coral/)

### Edgeworx Cloud
Deploy and manage edge applications including Darcy AI applications with the Edgeworx Cloud. Create an account for free at [https://cloud.edgeworx.io](https://cloud.edgeworx.io)

### Other helpful links
- Company website for Edgeworx, the providers of the Darcy AI platform [https://edgeworx.io](https://edgeworx.io)
- Official website for the Tensorflow AI project [https://www.tensorflow.org](https://www.tensorflow.org)
