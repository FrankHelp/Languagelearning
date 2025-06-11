public class PromptHandler
{

    // private string _prompt1 = "DON'T USE MARKDOWN! DON'T USE EMOJIS! Tu es un professeur de français amical, patient et jovial.";
    // private string _userPrompt1 = "Salue-moi et discute avec moi pour mieux me connaître, comme mon nom, mes origines culturelles et pourquoi j’apprends l’français. Pose une question à la fois et attends ma réponse avant de continuer. Si tu connais mes origines culturelles, salue-moi dans la langue de cette culture.";

    private string _prompt1 = "BENUTZE KEIN MARKDOWN! BENUTZE KEINE EMOJIS! Du bist ein freundlicher KI-Agent zum französischlernen und interagierst mit dem User im Rahmen einer Studie. Du antwortest nur auf deutsch.";
    private string _userPrompt1 = "Begrüße mich und erkläre dass ich an einer Studie teilnehme. Unterhalte dich mit mir um mich kennenzulernen, zum Beispiel meinen Namen und wieso ich französisch lernen will. Frag eine Frage auf einmal und warte auf meine Antwort bevor du fortfährst.";


    private string _prompt2 = "NE PAS UTILISER DE MARKDOWN ! NE PAS UTILISER D'EMOJIS ! Tu es un agent IA sympathique pour apprendre le français. TU RÉPONDS SEULEMENT EN FRANÇAIS, PAS EN ALLEMAND. Tu reponds avec un langage très simple. Les utilisateurs de niveau A1 doivent te comprendre.";
    private string _userPrompt2 = "Dis-moi de me présenter encore une fois, je dois essayer en français cette fois. Si les phrases sont difficiles pour moi, aide-moi s'il te plaît.";
    // private string _prompt2 = "DON'T USE MARKDOWN! DON'T USE EMOJIS! Tu es un professeur de français qui évalue le niveau de langue de l'utilisateur. Tu es familier avec les critères du CECR disponibles sur ce site : [CEFR Criteria](https://www.coe.int/en/web/common-european-framework-reference-languages/table-3-cefr-3.3-common-reference-levels-qualitative-aspects-of-spoken-language-use).";
    // private string _userPrompt2 = "Résume nos conversations précédentes en une phrase. Voici les conversations précédentes. Passe à l’évaluation de mon niveau de langue. Demande-moi de décrire une expérience mémorable et donne-moi un résultat basé sur les critères du CECR disponibles sur ce site : [CEFR Criteria](https://www.coe.int/en/web/common-european-framework-reference-languages/table-3-cefr-3.3-common-reference-levels-qualitative-aspects-of-spoken-language-use).";

    private string _prompt3 = "DON'T USE MARKDOWN! DON'T USE EMOJIS! Tu es un professeur de français amical, patient et jovial. Évaluez le niveau linguistique de l'utilisateur en vous basant sur l'échange précédent et restez cohérent avec le niveau que vous avez identifié. Tu demandes à l'utilisateur de choisir un scénario de jeu de rôle. Tu reponds seulement en francais.";
    private string _userPrompt3 = "Convaincs-moi de participer à un jeu de rôle pour pratiquer mon français. Propose-moi trois scénarios de la vie réelle que je peux pratiquer. Par exemple, commander de la nourriture au restaurant, un entretien d'embauche, ou voyager dans un pays anglophone. Ne les liste pas avec des numéros.";

    private string _prompt4 = "DON'T USE MARKDOWN! DON'T USE EMOJIS! Tu es un professeur de français amical, patient et jovial. Tu donnes un retour sur les pratiques de conversation en français de l'utilisateur.";
    private string _userPrompt4 = "Sur la base des pratiques de jeu de rôle précédentes. Résume le vocabulaire, la grammaire ou les phrases que l’utilisateur a appris pour une révision future. Le retour doit suivre ce format :\n**RETROACTION GÉNÉRALE** : Évalue la performance selon la leçon, cite une chose que l’élève a bien réussie, et une chose à améliorer.\n**CONSEILS POUR LA SUITE** : Donne des conseils à l’élève pour appliquer la leçon dans des situations réelles.";

    private int _currentPrompt = 1;
    private int _promptSaturationThreshold = 3;
    private int _messageCount = 0;

    public PromptHandler()
    {
    }

    public bool CheckForPromptSwitch()
    {
        // Check if we've reached the saturation threshold
        if (_messageCount >= _promptSaturationThreshold)
        {
            _currentPrompt++;
            _messageCount = 0; // Reset counter
            
            // Ensure we don't go beyond our prompt count
            if (_currentPrompt > 4) _currentPrompt = 1;
            return true;
        }else 
        {
            return false;
        }
    }

    public string GetCurrentSystemPrompt()
    {
        _messageCount++;
        return _currentPrompt switch
        {
            1 => _prompt1,
            2 => _prompt2,
            3 => _prompt3,
            4 => _prompt4,
            _ => _prompt1 // Default to first prompt
        };
    }

    public string GetCurrentUserPrompt()
    {
        // if (_currentPrompt == 2)
        // {
        //     // For prompt 2, we need to include previous conversation info
        //     return _userPrompt2.Replace("{user_info_conversation}", GetConversationSummary());
        // }

        return _currentPrompt switch
        {
            1 => _userPrompt1,
            2 => _userPrompt2,
            3 => _userPrompt3,
            4 => _userPrompt4,
            _ => _userPrompt1 // Default to first prompt
        };
    }
}
// IM ENDEFFEKT will ich ja den passenden systemprompt bekommen; und wenn die saturation erreicht ist, 
// nach der chatgpt antwort direkt eine neue anfrage senden mit dem nächsten system prompt + user prompt
// Dabei sollte der record button auch deaktiviert sein.