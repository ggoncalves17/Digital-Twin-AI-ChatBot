import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { BotMessageSquare } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import axios from 'axios';
import { toast } from "sonner";

const registerSchema = z.object({
  name: z.string().min(2, { message: "O nome deve ter pelo menos 2 caracteres" }),
  email: z.string().email({ message: "Email inválido" }),
  password: z.string().min(8, { message: "A senha deve ter pelo menos 8 caracteres" }),
  confirmPassword: z.string(),
  birthDate: z.string().refine((date) => {
    const selectedDate = new Date(date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return selectedDate <= today;
  }, { message: "A data de nascimento não pode ser futura" }),
}).refine((data) => data.password === data.confirmPassword, {
  message: "As senhas não coincidem",
  path: ["confirmPassword"],
});

const Register = () => {
  const navigate = useNavigate();

  const form = useForm<z.infer<typeof registerSchema>>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: "",
      password: "",
      ...({ name: "", confirmPassword: "", birthDate: "" }),
    },
  });

  const handleSubmit = async (values: z.infer<typeof registerSchema>) => {
    try {
      const response = await axios.post("http://localhost:8000/api/v1/users/register", {
        name: values.name, 
        birthdate: values.birthDate, 
        email: values.email, 
        password: values.password,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      toast.success("Utilizador registado com sucesso!");
      navigate("/");
 
    } catch (error: any) {
      if (error.response?.status === 404) {
        toast.error(error.response.data.detail);
      } else {
        console.log("ERRO: ", error)
        toast.error("Erro ao tentar registar utilizador.");
      }
    }
    };

  const toggleMode = () => {
    navigate("/");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-background via-background to-primary/5 p-4">
      <div className="absolute right-4 top-4">
        <ThemeToggle />
      </div>
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="space-y-2 text-center">
          <div className="mx-auto mb-2 flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
            <BotMessageSquare className="h-8 w-8 text-primary" />
          </div>
          <CardTitle className="text-3xl font-bold">Digital Twin</CardTitle>
          <CardDescription className="text-base">
            {"Crie sua conta"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nome</FormLabel>
                    <FormControl>
                      <Input placeholder="Seu nome" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input type="email" placeholder="seu@email.com" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Senha</FormLabel>
                    <FormControl>
                      <Input type="password" placeholder="••••••••" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <>
                <FormField
                  control={form.control}
                  name="confirmPassword"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Confirmar Senha</FormLabel>
                      <FormControl>
                        <Input type="password" placeholder="••••••••" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="birthDate"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Data de Nascimento</FormLabel>
                      <FormControl>
                        <Input type="date" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </>
              <Button type="submit" className="w-full">
                {"Criar Conta"}
              </Button>
            </form>
          </Form>
          <div className="mt-4 text-center text-sm">
            <button
              onClick={toggleMode}
              className="text-muted-foreground hover:text-primary transition-colors"
            >
              {"Já tem uma conta? Entrar"}
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Register;
