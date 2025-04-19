import React from "react";

interface MessageProps {
  content: string;
  isUserMessage: boolean;
}

const MessageBubble: React.FC<MessageProps> = React.memo(({ content, isUserMessage }) => {
  if (isUserMessage) {
    return <div className="user-message">{content}</div>;
  } else {
    return <div dangerouslySetInnerHTML={{ __html: content }} />;
  }
});

export default MessageBubble;
