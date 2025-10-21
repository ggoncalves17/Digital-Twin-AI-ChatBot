import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Send, User, Bot } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useNavigate } from "react-router-dom";
import axios from "axios";

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
  const navigate = useNavigate();

  // Protected Route for only autheticated users
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token == null) {
      navigate("/");
      return
    }

    axios.get('http://localhost:8000/api/v1/users/profile',
      { headers: { Authorization: `Bearer ${token}` } }
    )
      .then(function (response) {
      })
      .catch(function (error) {
        console.log(error);
        if (error.status == 401) {
          navigate("/");
        }
      });
  }, []);

  // Get all personas available
  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/personas/',
    )
      .then(function (response) {
        const data = response.data

        const personas: Persona[] = data.map((item: any) => ({
          id: item.id,
          name: item.name,
        }));

        setPersonas(personas)
      })
      .catch(function (error) {
        console.log(error);
      });
  }, [])

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `Como ${personas.find(p => p.id === selectedPersona)?.name}, estou aqui para ajudar!`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);
    }, 1000);
  };

  const currentPersona = personas.find(p => p.id === selectedPersona);

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

          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {!selectedPersona ? (
                <div className="flex h-full items-center justify-center text-center text-muted-foreground">
                  <div>
                    <Bot className="mx-auto mb-2 h-12 w-12 opacity-50" />
                    <p>Please select a persona to start the conversation.</p>
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
                messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"
                      }`}
                  >
                    {message.role === "assistant" && (
                      <Avatar className="h-8 w-8">
                        <AvatarFallback className="bg-primary/10">👤</AvatarFallback>
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
                ))
              )}
            </div>
          </ScrollArea>


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
