import { DragEvent, KeyboardEvent, useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";

interface Message {
  id: number;
  content: string;
  isUserMessage: boolean;
}

function App() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [thinking, setThinking] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const conversationBottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    conversationBottomRef.current?.scrollIntoView({ behavior: "smooth"});
  }, [messages, thinking])

  const handleFileUpload = (
    event: DragEvent<HTMLDivElement> | React.ChangeEvent<HTMLInputElement>
  ) => {
    let file: File | null = null;

    if ("dataTransfer" in event && event.dataTransfer) {
      file = event.dataTransfer.files[0];
    } else if (
      "target" in event &&
      event.target &&
      (event.target as HTMLInputElement).files &&
      (event.target as HTMLInputElement).files?.length
    ) {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        file = target.files[0];
      }
    }

    if (file) {
      setUploadedFile(file);
    }
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
  };

  const handleSubmit = async () => {
    const currentInputValue = inputRef.current?.value || "";
    console.log(uploadedFile);
    console.log(currentInputValue);
    if (!uploadedFile && currentInputValue.trim() === "") return;

    try {
      if (currentInputValue !== "")
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: prevMessages.length,
            content: currentInputValue,
            isUserMessage: true,
          },
        ]);

      const formData = new FormData();
      formData.append("prompt", currentInputValue);

      if (uploadedFile) {
        formData.append("file", uploadedFile);
      }

      console.log("Sending request");

      if (inputRef.current) {
        inputRef.current.value = "";
      }
      setThinking(true);
      setUploadedFile(null);

      const response = await fetch("http://localhost:8000/interact", {
        method: "POST",
        body: formData,
      });

      console.log("Request sent");

      if (!response.ok) {
        throw new Error(
          "Something went wrong while sending request to backend!!"
        );
      }

      const data = await response.json();
      console.log("Response:", data);
      setThinking(false);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: prevMessages.length,
          content: data.message,
          isUserMessage: false,
        },
      ]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleKeyPress = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSubmit();
    }
  };

  const handleDragOver = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    handleFileUpload(event);
  };

  return (
    <div className="app">
      <div className="bg-image"></div>

      <div
        className="chatbot-container"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <div className="conversation-container">
          {messages.map((message: Message) => (
            <MessageBubble
              key={message.id}
              content={message.content.replace("```", "").replace("```", "").replace("html", "")}
              isUserMessage={message.isUserMessage}
            />
          ))}
          {messages.length === 0 && !thinking && (
            <div className="welcome-message">Welcome to Concerts RAG</div>
          )}
          {thinking && <p className="thinking-message">Thinking...</p>}

          <div ref={conversationBottomRef} />
        </div>

        {uploadedFile && (
          <div className="uploaded-file">
            <i className="fa-regular fa-file" onClick={handleRemoveFile} />
            {uploadedFile.name}
            <i className="fas fa-times" onClick={handleRemoveFile} />
          </div>
        )}

        <div className="control-buttons">
          <input
            ref={inputRef}
            type="text"
            placeholder="Type something or drop document"
            onKeyDown={handleKeyPress}
          />
          <button onClick={handleSubmit}>
            <i className="fa-regular fa-paper-plane" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
