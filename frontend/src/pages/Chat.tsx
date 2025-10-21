import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Send, User, Bot } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
};

type Persona = {
  id: string;
  name: string;
  description: string;
  icon: string;
};

const personas: Persona[] = [
  { id: "assistant", name: "Assistente", description: "Ajudante geral", icon: "🤖" },
  { id: "teacher", name: "Professor", description: "Educador paciente", icon: "👨‍🏫" },
  { id: "coach", name: "Coach", description: "Motivador de vida", icon: "💪" },
  { id: "analyst", name: "Analista", description: "Pensador crítico", icon: "📊" },
];

const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [selectedPersona, setSelectedPersona] = useState<string>("assistant");

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

    // Simular resposta do bot
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

  return (
    <div className="flex h-screen bg-gradient-to-br from-background via-background to-primary/5">
      <div className="absolute right-4 top-4">
        <ThemeToggle />
      </div>

      <div className="container mx-auto flex h-full max-w-6xl gap-4 p-4">
        {/* Sidebar de Personas */}
        <Card className="w-72 p-4">
          <div className="mb-4">
            <h2 className="mb-2 text-lg font-semibold">Persona Ativa</h2>
            <Select value={selectedPersona} onValueChange={setSelectedPersona}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {personas.map((persona) => (
                  <SelectItem key={persona.id} value={persona.id}>
                    <div className="flex items-center gap-2">
                      <span className="text-xl">{persona.icon}</span>
                      <span>{persona.name}</span>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="rounded-lg bg-secondary/50 p-4">
            <div className="mb-2 text-4xl">{currentPersona?.icon}</div>
            <h3 className="mb-1 font-semibold">{currentPersona?.name}</h3>
            <p className="text-sm text-muted-foreground">{currentPersona?.description}</p>
          </div>
        </Card>

        {/* Área de Chat */}
        <Card className="flex flex-1 flex-col">
          {/* Header */}
          <div className="border-b border-border p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-2xl">
                {currentPersona?.icon}
              </div>
              <div>
                <h1 className="text-xl font-bold">Digital Twin</h1>
                <p className="text-sm text-muted-foreground">
                  Conversando como {currentPersona?.name}
                </p>
              </div>
            </div>
          </div>

          {/* Mensagens */}
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {messages.length === 0 && (
                <div className="flex h-full items-center justify-center text-center text-muted-foreground">
                  <div>
                    <Bot className="mx-auto mb-2 h-12 w-12 opacity-50" />
                    <p>Comece uma conversa com o Digital Twin</p>
                  </div>
                </div>
              )}
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  {message.role === "assistant" && (
                    <Avatar className="h-8 w-8">
                      <AvatarFallback className="bg-primary/10">
                        {currentPersona?.icon}
                      </AvatarFallback>
                    </Avatar>
                  )}
                  <div
                    className={`max-w-[70%] rounded-lg px-4 py-2 ${
                      message.role === "user"
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
            </div>
          </ScrollArea>

          {/* Input */}
          <div className="border-t border-border p-4">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex gap-2"
            >
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Digite sua mensagem..."
                className="flex-1"
              />
              <Button type="submit" size="icon">
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
