package com.yourway.alert.repository;

import com.yourway.alert.domain.Query;
import org.springframework.data.jpa.repository.*;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Spring Data SQL repository for the Query entity.
 */
@SuppressWarnings("unused")
@Repository
public interface QueryRepository extends JpaRepository<Query, Long> {
    List<Query> findAllByUserId(Integer userId);

    Query findByQueryId(Integer queryId);
}
