def scoring_criteria(answer_score, video_scores):
    net_score = answer_score
    if video_scores > 0.5:
        net_score = net_score - 0.01 * video_scores
    return net_score