package yourway.api.repository;

import models.UserQuery;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface UserQueryRepository extends CrudRepository<UserQuery, Integer> {
    List<UserQuery> findAllByUserId(Integer userId);

    UserQuery findByQueryId(Integer queryId);
}