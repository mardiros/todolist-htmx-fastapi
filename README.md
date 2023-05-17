# todolist-htmx-fastapi

A dummy todolist using htmx client side, fast api server side.
The todolist is stored in memory, this project is about starts learning htmx basics.

## Prerequisites

Every commands are bound in a [Justfile](https://github.com/mardiros/todolist-htmx-fastapi/blob/main/Justfile).
That are interpreted by the commander runner [just](https://github.com/casey/just)

## Installation

```bash
just install
```

## Run the test suite

```bash
just test
```

## Start

Because it is a project to evaluate htmx, there is no start command,
there is just a command to serve the website and run a web browser.


```bash
just funcdevtest
```

### Demo

![Demo Of The TODO](https://raw.githubusercontent.com/mardiros/todolist-htmx-fastapi/main/demo.gif)