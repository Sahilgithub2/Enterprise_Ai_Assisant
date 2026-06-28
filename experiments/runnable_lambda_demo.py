from langchain_core.runnables import RunnableLambda

def hello(x):
    return "Alice"  +' '+str(x**2)

runnable = RunnableLambda(hello)

print(runnable.invoke(10))
