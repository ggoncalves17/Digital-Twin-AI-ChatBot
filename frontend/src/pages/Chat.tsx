import { useEffect, useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Send, User, Bot } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useNavigate } from "react-router-dom";
import api from "@/api/axios";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
};

type Persona = {
  id: string;
  name: string;
};

const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [selectedPersona, setSelectedPersona] = useState<string>("");
  const [userId, setUserId] = useState<string | null>(null);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const navigate = useNavigate();

  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Get authenticated user profile
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
      return;
    }

    api
      .get("/api/v1/users/profile", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => {
        setUserId(response.data.id);
      })
      .catch((error) => {
        console.error("Failed to load profile:", error);
        if (error.response?.status === 401) {
          navigate("/");
        }
      });
  }, []);

  // Get all personas
  useEffect(() => {
    api
      .get("/api/v1/personas/")
      .then((response) => {
        const personas: Persona[] = response.data.map((item: any) => ({
          id: item.id,
          name: item.name,
        }));
        
        personas.unshift({ id: "supervisor", name: "Supervisor" });

        setPersonas(personas);
      })
      .catch((error) => {
        console.error("Failed to load personas:", error);
      });
  }, []);

  // Fetch chat history when a persona is selected
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!selectedPersona || !userId || !token) {
      setMessages([]);
      return;
    }

    if (selectedPersona.toLowerCase() === "supervisor") {
      setMessages([]);
      return;
    }

    setLoadingHistory(true);

    api
      .get(
        `/api/v1/users/${userId}/chats/${selectedPersona}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      .then((response) => {
        const loadedMessages: Message[] = response.data.map((msg: any) => ({
          id: msg.id.toString(),
          role: msg.role.toLowerCase() === "user" ? "user" : "assistant",
          content: msg.content,
          timestamp: new Date(msg.created_at),
        }));
        setMessages(loadedMessages);
      })
      .catch((error) => {
        console.error("Failed to load chat history:", error);
        setMessages([]);
      })
      .finally(() => {
        setLoadingHistory(false);
      });
  }, [selectedPersona, userId]);

const handleSend = async () => {
  if (!input.trim() || !userId || !selectedPersona) return;

  const userMessage: Message = {
    id: Date.now().toString(),
    role: "user",
    content: input,
    timestamp: new Date(),
  };

  setMessages((prev) => [...prev, userMessage]);
  const messageContent = input;
  setInput("");
  setIsBotTyping(true);

  try {
    const token = localStorage.getItem("token");

    let url = "";

    if (selectedPersona === "supervisor") {
      url = `/api/v1/users/${userId}/multi-agent`;
    } else {
      url = `/api/v1/users/${userId}/chats/${selectedPersona}`;
    }

    const response = await api.post(
      url,
      { role: "User", content: messageContent },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = response.data;

    const assistantMessage: Message = {
      id: data.id.toString(),
      role: data.role.toLowerCase() === "assistant" ? "assistant" : "user",
      content: data.content,
      timestamp: new Date(data.created_at),
    };

    setMessages((prev) => [...prev, assistantMessage]);
  } catch (error) {
    console.error("Failed to send message:", error);

    const errorMessage: Message = {
      id: Date.now().toString() + "-error",
      role: "assistant",
      content: "Failed to get a response from the assistant.",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, errorMessage]);
  } finally {
    setIsBotTyping(false);
  }
};


  const currentPersona = personas.find((p) => p.id === selectedPersona);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-background via-background to-primary/5">
      <div className="absolute right-4 top-4 flex gap-2">
        <ThemeToggle />
        <Button variant="outline" onClick={handleLogout}>
          Logout
        </Button>
      </div>

      <div className="container mx-auto flex h-full max-w-6xl gap-4 p-4">
        {/* Sidebar */}
        <Card className="w-72 p-4">
          <div className="mb-4">
            <h2 className="mb-2 text-lg font-semibold">Personas</h2>
            <Select value={selectedPersona} onValueChange={setSelectedPersona}>
              <SelectTrigger>
                <SelectValue placeholder="Select a user" />
              </SelectTrigger>
              <SelectContent>
                {personas.map((persona) => (
                  <SelectItem key={persona.id} value={persona.id}>
                    <div className="flex items-center gap-2">
                      <span className="text-xl">👤</span>
                      <span>{persona.name}</span>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </Card>

        {/* Chat panel */}
        <Card className="flex flex-1 flex-col">
          <div className="border-b border-border p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-2xl">
                👤
              </div>
              <div>
                <h1 className="text-xl font-bold">
                  {currentPersona?.name || "No Persona selected"}
                </h1>
              </div>
            </div>
          </div>

          {/* Chat messages */}
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {!selectedPersona ? (
                <div className="flex h-full items-center justify-center text-center text-muted-foreground">
                  <div>
                    <Bot className="mx-auto mb-2 h-12 w-12 opacity-50" />
                    <p>Please select a persona to start the conversation.</p>
                  </div>
                </div>
              ) : loadingHistory ? (
                <div className="flex h-full items-center justify-center text-center text-muted-foreground">
                  <div>
                    <Bot className="mx-auto mb-2 h-12 w-12 animate-spin opacity-50" />
                    <p>Loading chat...</p>
                  </div>
                </div>
              ) : messages.length === 0 ? (
                <div className="flex h-full items-center justify-center text-center text-muted-foreground">
                  <div>
                    <Bot className="mx-auto mb-2 h-12 w-12 opacity-50" />
                    <p>Start a new conversation</p>
                  </div>
                </div>
              ) : (
                <>
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"
                        }`}
                    >
                      {message.role === "assistant" && (
                        <Avatar className="h-8 w-8">
                          <AvatarFallback className="bg-primary/10">🤖</AvatarFallback>
                        </Avatar>
                      )}
                      <div
                        className={`max-w-[70%] rounded-lg px-4 py-2 ${message.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-secondary"
                          }`}
                      >
                        <p className="text-sm">{message.content}</p>
                      </div>
                      {message.role === "user" && (
                        <Avatar className="h-8 w-8">
                          <AvatarFallback className="bg-primary/10">
                            <User className="h-4 w-4" />
                          </AvatarFallback>
                        </Avatar>
                      )}
                    </div>
                  ))}

                  {isBotTyping && (
                    <div className="flex gap-3 justify-start">
                      <Avatar className="h-8 w-8">
                        <AvatarFallback className="bg-primary/10">🤖</AvatarFallback>
                      </Avatar>
                      <div className="max-w-[70%] rounded-lg bg-secondary px-4 py-2">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <span>Typing</span>
                          <svg
                            className="h-4 w-4 animate-spin text-muted-foreground"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                          >
                            <circle
                              className="opacity-25"
                              cx="12"
                              cy="12"
                              r="10"
                              stroke="currentColor"
                              strokeWidth="4"
                            />
                            <path
                              className="opacity-75"
                              fill="currentColor"
                              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                            />
                          </svg>
                        </div>
                      </div>
                    </div>
                  )}

                  <div ref={bottomRef} />
                </>
              )}
            </div>
          </ScrollArea>

          {/* Input */}
          <div className="border-t border-border p-4">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (selectedPersona) handleSend();
              }}
              className="flex gap-2"
            >
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={
                  selectedPersona ? "Write your message..." : "Select a persona first"
                }
                className="flex-1"
                disabled={!selectedPersona}
              />
              <Button type="submit" size="icon" disabled={!selectedPersona}>
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Chat;
