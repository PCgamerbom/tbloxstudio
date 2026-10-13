# T-BloxStudio

O `T-BloxStudio.exe` abre a versao mais recente do Roblox Studio encontrada em `%LOCALAPPDATA%\Roblox\Versions`, `%ProgramFiles%\Roblox\Versions` ou `%ProgramFiles(x86)%\Roblox\Versions`, instala o plugin automaticamente e encaminha os argumentos recebidos ao Studio. O plugin vai embutido no launcher. Se nao houver uma instalacao oficial, o launcher procura `RobloxStudioBeta.exe` ao lado dele.

Execute `T-BloxStudio.exe` no Windows. No Studio, abra o botao **T-BloxStudio** na barra de plugins e escolha uma das paletas. A escolha fica salva entre sessoes. O arquivo `.bat` continua disponivel como alternativa de desenvolvimento.

Para compilar o executavel Windows x64 com o SDK .NET 10, rode `dotnet publish T-BloxStudio.Launcher/T-BloxStudio.Launcher.csproj -c Release -r win-x64 --self-contained true -o dist`. O resultado e `dist/T-BloxStudio.exe`.

O workflow do GitHub Actions tambem compila no Windows a cada alteracao relevante em `main`. Para baixar o resultado, abra **Actions**, escolha a execucao mais recente de **Build T-BloxStudio for Windows** e baixe o artefato **T-BloxStudio-Windows-x64**.

O T-BloxStudio e um launcher: ele abre a instalacao oficial sem substitui-la nem alterar seus binarios. As paletas personalizam somente o painel do plugin; a interface nativa e o motor do Roblox Studio nao sao alterados.

Se o launcher mostrar um erro, os detalhes ficam em `%LOCALAPPDATA%\T-BloxStudio\launcher.log`.

Para remover o plugin, feche o Studio e apague `%LOCALAPPDATA%\Roblox\Plugins\TBloxStudio.lua`.