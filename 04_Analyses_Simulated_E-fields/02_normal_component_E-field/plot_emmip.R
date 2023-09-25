emms_generate <- function(model,path,A,B,C,D){
    Limit <- 25000
    if (missing(B) & missing(C) & missing(D)) {
    emm_f <- as.formula(paste0("pairwise ~ ", A));
    Parameter <- A
    reduce <- -1    
    
    } else if (!(missing(B)) & missing(C) & missing(D)) {
    emm_f <- as.formula(paste0("pairwise ~ ", A, "|",B));
    Parameter <- paste0(A,"_",B)
    reduce <- -2

    } else if (!(missing(B)) & !(missing(C)) & missing(D)) {
    emm_f <- as.formula(paste0("pairwise ~ ", A, "|",B ,"*", C));
    Parameter <- paste0(A, "_", B, "_", C)
    reduce <- -4
    }
    else {
    emm_f <- as.formula(paste0("pairwise ~ ", A, "|",B , "*", C, "*", D));
    Parameter <- paste0(A, "_", B, "_", C, "_", D)
    reduce <- -8
    }

emm_s <- emmeans(model, adjust = "Tukey",
                 pbkrtest.limit = Limit, 
                 specs = emm_f,
                 frequenttist=TRUE)
emm_s.posthoc <- pairs(emm_s)
#summary(emm_s.posthoc)
emm_s.posthoc <- as.data.frame(emm_s.posthoc)

View(emm_s.posthoc)

emm_s <- as.data.frame(emm_s)
emm_s <- emm_s %>% mutate(across(where(is.numeric), ~round(., digits = digits)))
emm_s.posthoc <- emm_s.posthoc %>% mutate(across(where(is.numeric), ~round(., digits = digits2)))

# To save all EMM tables and posthoc parameter activate the 2 lines of code by deleting ##

write.csv(emm_s.posthoc, file.path(path, paste0("EMM_Posthoc_",Parameter,".csv")))
write.csv(emm_s, file.path(path, paste0("EMM_Table_",Parameter,".csv")))

View(reduce)
emm_s.r <- head(emm_s, reduce)

View(emm_s.r)

return(emm_s.r)
}


plot_posthoc <- function(df, emm, Interaction, COLOR, xtitle)
{Interaction <- enquo(Interaction)
#df <- df[df[[Factor]] == level,]
#emm <- emm[emm[[Factor]] == level,]
g <- ggplot() + 
    ylim(0, 0.35) +
    theme_classic() +
    theme(panel.grid = element_line(), panel.grid.major = element_line(),
    panel.border = element_rect(colour = "black", fill = NA, size = 1)) +
    geom_violinhalf(data = df,
        aes(x = !!Interaction, y = meanNormalE, fill = !!Interaction),
        flip = c(1, 3), trim = FALSE, alpha = 0.3) +
        scale_fill_grey(start = 0.01,
        end = 0.6) +
    geom_point(data = df,
         aes(x = !!Interaction, y = meanNormalE, color = !!Interaction),
        size = 1, alpha = 0.3, position = position_jitter(w = 0.025, h = 0)
         ) +
        scale_y_continuous(name = ylab_text ,
       sec.axis = sec_axis(trans=~.*1, 
        name = ylab_LMM_text), limits = c(0, 0.35)) +
        scale_colour_grey(start = 0.01,
        end = 0.35) +
    geom_point(data = emm,
        aes(x = !!Interaction, y = emmean, group = !!Interaction),
        size = 3, position = position_dodge(0.8)) +
    geom_line(data = emm,
    aes(x = !!Interaction, y = emmean, group = 1), size = 1, color = COLOR) +
    scale_colour_grey(start = 0.01,
  end = 0.35) +
    geom_errorbar(data = emm,
       aes(x = !!Interaction, y = emmean, ymin = lower.CL, ymax = upper.CL), 
        width = 0.2, linewidth = 2,
    position = position_dodge(0.8), color = COLOR) +
    theme(axis.text.y.right = element_text(color = COLOR),
      axis.title.y.right = element_text(colour = COLOR)) +
    theme(text = element_text(family = "DejaVuSans", size = fontsize_2)) +
    theme(legend.position = "none") +
    xlab(xtitle) +
    theme(panel.grid = element_line(), panel.grid.major = element_line(),
    panel.border = element_rect(colour = "black", fill = NA, size = 1))
    return(g)
}

plot_posthoc_multi <- function(df, emm, Interaction, 
Factor1, level1, Factor2, level2,
Numb, xtitle, facet1, facet2, COLOR)

{Interaction <- enquo(Interaction)
 facet1 <- enquo(facet1)
 facet2 <- enquo(facet2)
df <- df[df[[Factor1]] == level1 & df[[Factor2]] == level2,]
emm <- emm[emm[[Factor1]] == level1 & emm[[Factor2]] == level2,]

g <- ggplot() +
  ylim(-0.1, 0.35) +
   theme_classic() +
    theme(panel.grid = element_line(linewidth = 0.5, linetype = 'solid',
                                colour = "grey")) +
    geom_violinhalf(data = df,
        aes(x = !!Interaction, y = meanNormalE, fill = !!Interaction),
        flip = c(1, 3), trim = FALSE, alpha = 0.3) +
        scale_fill_grey(start = 0.01,
  end = 0.6) +
    geom_point(data = df,
         aes(x = !!Interaction, y = meanNormalE, color = !!Interaction),
        size = 1, alpha = 0.5, position = position_jitter(w = 0.025, h = 0)
         ) +
    geom_point(data = emm,
        aes(x = !!Interaction, y = emmean, group = !!Interaction),
        size = 3, position = position_dodge(0.8), color = COLOR) +
    geom_line(data = emm,
    aes(x = !!Interaction, y = emmean, group = 1), size = 1, color = COLOR) +
    scale_colour_grey(start = 0.01,
  end = 0.35) +
    geom_errorbar(data = emm,
        aes(x = !!Interaction, y = emmean, ymin = lower.CL, ymax = upper.CL), 
        width = 0.2, linewidth = 2, color = COLOR,
    position = position_dodge(0.8)) +
    theme(text = element_text(family = "DejaVuSans", size = fontsize)
        ) +
     theme(legend.position = "none")
    if (Numb  == "4") {
      g <-  g +
         theme(legend.position = "none",
     axis.title.y = element_blank(),
     axis.title.x = element_blank())+
      scale_y_continuous(name = ylab_LMM_text,
      position = "right", limits = c(-0.01, 0.35)) +
      theme(axis.text.y.right = element_text(color = COLOR),
      axis.title.y.right = element_blank()) +
      facet_grid(vars(!!facet1)) +
      #lab(xtitle) +
    theme(panel.grid = element_line(), panel.grid.major = element_line(),
    panel.border = element_rect(colour = "black", fill = NA, size = 1))
    } else if (Numb  == "1")      {
     g <- g +
     theme(legend.position = "none",
     axis.text.x = element_blank(),
     axis.ticks.x = element_blank(),
     axis.title.x = element_blank(),
     axis.line.x = element_blank(),
     axis.title.y = element_blank()) +
    scale_y_continuous(name = ylab_text, limits = c(-0.01, 0.35)) +
    facet_grid(, vars(!!facet2)) +
    theme(panel.grid = element_line(), panel.grid.major = element_line(),
    panel.border = element_rect(colour = "black", fill = NA, size = 1))
    } else if (Numb  == "2") {
     g <- g +
     theme(legend.position = "none",
     axis.text.x = element_blank(),
     axis.ticks.x = element_blank(),
     axis.title.x = element_blank(),
     axis.line.x = element_blank()) +
     scale_y_continuous(name = ylab_LMM_text,
     position = "right", limits = c(-0.01, 0.35)) +
      theme(axis.text.y.right = element_text(color = COLOR),
      axis.title.y.right = element_blank())  +
    facet_grid(vars(!!facet1), vars(!!facet2)) +
    theme(panel.grid = element_line(), panel.grid.major = element_line(),
    panel.border = element_rect(colour = "black", fill = NA, size = 1))
    } else if (Numb == "3") {
     g <- g +
     theme(legend.position = "none",
     axis.title.y = element_blank(),
     axis.title.x = element_blank())+
    scale_y_continuous(name = ylab_text, limits = c(-0.01, 0.35)) +
    theme(panel.grid = element_line(), panel.grid.major = element_line(),
    panel.border = element_rect(colour = "black", fill = NA, size = 1)) +
    xlab(xtitle)
    }    

     return(g)
}




grid_arrange <- function(fig1,fig2,fig3,fig4,xlabel,save_fig){

left <-  textGrob(ylab_text, rot=90, gp=gpar(fontface = 0, fontsize = fontsize))
right <- textGrob( ylab_LMM_text, rot=-90, gp = gpar(col = "blue", fontface = 3, fontsize = fontsize))
bottom <- textGrob( xlabel, gp=gpar(fontface = 0,fontsize = fontsize))

fig <- grid.arrange(patchworkGrob(fig1 + fig2 + fig3 + fig4),
left = left,
right = right,
bottom = bottom)
ggsave(file.path(path_images,
save_fig),
 width = width, 
 height = height, 
 dpi = dpi*4, 
 fig)
}


