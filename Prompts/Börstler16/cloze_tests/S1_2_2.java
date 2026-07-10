/** 
 * Informs the webmaster of an unexpected problem (Exception “ex”) 
 * with the deployed application (indicated by “aRequest”). 
 */ 
public void logAndEmailSeriousProblem(Throwable ex, HttpServletRequest aRequest) 
{ 
    /* Define local variable. */ 
    TroubleTicket troubleTicket = new TroubleTicket(ex, aRequest); 
    
    /* Log message. */ 
    fLogger.severe("TOP LEVEL CATCHING Throwable."); 
    fLogger.severe(troubleTicket.toString()); 
    
    /* Log message again. */ 
    log("SERIOUS PROBLEM OCCURRED."); 
    A:_____________________________; 
    
    /* Update context and mail trouble ticket. */ 
    HttpSession session = aRequest.getSession(); 
    B:_____________________ = session.C:_________________; 
    context.setAttribute(MOST_RECENT_TROUBLE_TICKET, troubleTicket);   
    troubleTicket.mailToWebmaster(); 
}